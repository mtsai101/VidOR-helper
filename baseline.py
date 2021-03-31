import os
import json
import argparse
import pickle as pkl
from collections import defaultdict

from tqdm import tqdm

from dataset import ImagenetVidVRD
from dataset import VidOR

from baseline import segment_video, get_model_path
from baseline import trajectory, feature, model, association

dataset = None
def load_object_trajectory_proposal(dataset):
    """
    Test loading precomputed object trajectory proposals
    """
    # dataset = ImagenetVidVRD('./vidvrd-dataset', './vidvrd-dataset/videos', ['train', 'test'])
    # dataset = VidOR('./vidor-dataset/annotation', './vidor-dataset/video', ['training', 'validation'])

    video_indices = dataset.get_index(split='training')
    for vid in video_indices:
        durations = set(rel_inst['duration'] for rel_inst in dataset.get_relation_insts(vid, no_traj=True))
        for duration in durations:
            segs = segment_video(*duration)
            for fstart, fend in segs:
                trajs = trajectory.object_trajectory_proposal(dataset, vid, fstart, fend, gt=False, verbose=True)
                trajs = trajectory.object_trajectory_proposal(dataset, vid, fstart, fend, gt=True, verbose=True)

    video_indices = dataset.get_index(split='validation')
    for vid in video_indices:
        anno = dataset.get_anno(vid)
        segs = segment_video(0, anno['frame_count'])
        for fstart, fend in segs:
            trajs = trajectory.object_trajectory_proposal(dataset, vid, fstart, fend, gt=False, verbose=True)
            trajs = trajectory.object_trajectory_proposal(dataset, vid, fstart, fend, gt=True, verbose=True)


def load_relation_feature(dataset):
    """
    Test loading precomputed relation features
    """
    # dataset = ImagenetVidVRD('./vidvrd-dataset', './vidvrd-dataset/videos', ['train', 'test'])
    # dataset = VidOR('./vidor-dataset/annotation', './vidor-dataset/video', ['training', 'validation'])

    extractor = feature.FeatureExtractor(dataset, prefetch_count=0)

    video_indices = dataset.get_index(split='training')
    for vid in video_indices:
        durations = set(rel_inst['duration'] for rel_inst in dataset.get_relation_insts(vid, no_traj=True))
        for duration in durations:
            segs = segment_video(*duration)
            for fstart, fend in segs:
                extractor.extract_feature(dataset, vid, fstart, fend, verbose=True)

    video_indices = dataset.get_index(split='validation')
    for vid in video_indices:
        anno = dataset.get_anno(vid)
        segs = segment_video(0, anno['frame_count'])
        for fstart, fend in segs:
            extractor.extract_feature(dataset, vid, fstart, fend, verbose=True)


def train(dataset):
    # dataset = ImagenetVidVRD('./vidvrd-dataset', './vidvrd-dataset/videos', ['train', 'test'])
    # dataset = VidOR('./vidor-dataset/annotation', './vidor-dataset/video', ['training', 'validation'])

    param = dict()
    param['model_name'] = 'baseline'
    param['rng_seed'] = 1701
    param['max_sampling_in_batch'] = 32
    param['batch_size'] = 64
    param['learning_rate'] = 0.001
    param['weight_decay'] = 0.0
    param['max_iter'] = 5000
    param['display_freq'] = 1
    param['save_freq'] = 5000
    param['epsilon'] = 1e-8
    param['pair_topk'] = 20
    param['seg_topk'] = 200
    

    model.train(dataset, param)


def detect(dataset):
    # dataset = ImagenetVidVRD('./vidvrd-dataset', './vidvrd-dataset/videos', ['train', 'test'])
    # dataset = VidOR('./vidor-dataset/annotation', './vidor-dataset/video', ['training', 'validation'])

    with open(os.path.join(get_model_path(), 'baseline_setting.json'), 'r') as fin:
        param = json.load(fin)
    short_term_relations = model.predict(dataset, param)
    # group short term relations by video
    video_st_relations = defaultdict(list)
    for index, st_rel in short_term_relations.items():
        vid = index[0]
        video_st_relations[vid].append((index, st_rel))
    # video-level visual relation detection by relational association
    print('greedy relational association ...')
    video_relations = dict()
    for vid in tqdm(video_st_relations.keys()):
        video_relations[vid] = association.greedy_relational_association(
                dataset, video_st_relations[vid], max_traj_num_in_clip=100)
    # save detection result
    with open(os.path.join(get_model_path(), 'baseline_relation_prediction.json'), 'w') as fout:
        output = {
            'version': 'VERSION 1.0',
            'results': video_relations
        }
        json.dump(output, fout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='VidOR baseline')
    parser.add_argument('--load_feature', action="store_true", default=False, help='Test loading precomputed features')
    parser.add_argument('--train', action="store_true", default=False, help='Train model')
    parser.add_argument('--detect', action="store_true", default=False, help='Detect video visual relation')
    args = parser.parse_args()


    dataset = VidOR('./vidor-dataset/annotation', './vidor-dataset/video', ['training','validation'])

    if args.load_feature or args.train or args.detect:
        if args.load_feature:
            load_object_trajectory_proposal(dataset)
            load_relation_feature(dataset)
        if args.train:
            train(dataset)
        if args.detect:
            detect(dataset)
    else:
        parser.print_help()
