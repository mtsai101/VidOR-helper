# Video Visual Relation Understanding Helpler

This repository is the modified version of [VidVRD-helper](https://github.com/NExTplusplus/VidVRD-helper), which is evaluation code of Video Relation Understanding, ACM Multimedia'21 Grand Challenge.
We update add a few features to help our students evaluate their own codes of the dataset [VidOR](https://xdshang.github.io/docs/vidor.html#downloads)

## Qucik Start
### Perequisites
You are encoraged to use your own virtual environment, e.g., Anaconda or virtualenv, to create a new and clean environment to develop.
For example, if you use virtualenv in Ubuntu, you need to create the env first:
```
python3 -m venv venv
```
And activate it:
```
source venv/bin/activate
```
We already export all the required packages to requirements.txt, just pip install them:
```
pip install -r requirements.txt
```

### Dataset
After installing the requirements, let's download the [VidOR dataset] (https://xdshang.github.io/docs/vidor.html#downloads) provided by Shang et al.
The recommand structure after you download all the videos and annotation is like:
```
VidVOR-helper
├── vidor-dataset
│   ├── annotation
│   │   ├── training
│   │   │   ├── 0000
│   │   │   └── ...
│   │   └── validation
│   │   │   ├── 0000
│   │   │   └── ...
│   └── video
│       ├── 0000
│       ├── 0001
│       ├── ...
├── doc
.
.
.
├── baseline.py
├── evaluate.py
└── visualize.py
```
Otherwise, you need to change the path in the specified scripts.

## Top-1 solution in ACM MM'19
This is just a sample starting point, you don't need to look into it necessarily. 
The top-1 solution of VRU'2019 was released at [link](https://zdtnag7mmr.larksuite.com/file/boxusugavBW2RyKEE277UdPROyb), including precomputed features, bounding box trajectories, and source code. 
Please cite this paper if you want to do this challenge based on their idea.

### How to
Here we just mention how to testing the pretrained model. Note that you will need to modifiy the feature extraction or re-build your own model. 
#### Features
Before testing, please generate the spatial and language feaures first.
```
python3 prepare.py
```
#### Testing
While testing, the flag **single_result_file** in vidor_config.yaml indicates the single or individual json files are generated.
```
python3 test.py
```
You will get ***~/vidvrd-mff/results/vidor_val_spalan.json*** or ***~/vidvrd-mff/results/vidor_val_spalan/XXXXXXX.json*** for the evaluation

## How to run this helper
### Evaluation
In this Grand Challenge, you need to generate a JSON file which cotains triplet, trajectory, and some other results. 
Please follow the submission format. (Find detailed format in [link](https://videorelation.nextcenter.org/mm21-gdc/task1.html))
You can evaluate all video by:
```
python3 evaluate.py [dataset] [split] [task] [prediction_json_annotation]
```
However, if you only want to evaluate one specified video without lengthy evaluation, add a flag **-s**
The following is the sample command:
```
python3 evaluate.py vidor validation relation ~/vidvrd-mff/results/vidor_val_spalan.json
python3 evaluate.py -s vidor validation relation ~/vidvrd-mff/results/vidor_val_spalan/2435633172.json
```
Please follow the official [Evaluation Metric](https://videorelation.nextcenter.org/mm21-gdc/task1.html)

### Visualization
The annotation of individual video is able to visualize the bounding box and relation:
```
python3 visualize.py [video_path] [annotation_path] [output_path]
```
Take one of the video in training set as example:
```
python3 visualize.py ~/VidOR-helper/vidor-dataset/video/ ~/VidOR-helper/vidor-dataset/annotation/training/0000/2401075277.json ~/output
```




Please cite the following papers if the datasets help your research:
```
@inproceedings{shang2017video,
    author={Shang, Xindi and Ren, Tongwei and Guo, Jingfan and Zhang, Hanwang and Chua, Tat-Seng},
    title={Video Visual Relation Detection},
    booktitle={ACM International Conference on Multimedia},
    address={Mountain View, CA USA},
    month={October},
    year={2017}
}

@inproceedings{shang2019annotating,
    author={Shang, Xindi and Di, Donglin and Xiao, Junbin and Cao, Yu and Yang, Xun and Chua, Tat-Seng},
    title={Annotating Objects and Relations in User-Generated Videos},
    booktitle={ACM International Conference on Multimedia Retrieval},
    address={Ottawa, ON, Canada},
    month={June},
    year={2019}
}
```

### Acknowledgement

This research is supported by the National Research Foundation, Singapore under its International Research Centres in Singapore Funding Initiative. Part of this research is also supported by National Science Foundation of China (61321491, 61202320), Collaborative Innovation Center of Novel Software Technology and Industrialization, and China Scholarship Council. Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not reflect the views of National Research Foundation, Singapore.
