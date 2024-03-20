# Bag Attention Network (BAN)

<details>
<summary>
    <b>Multiple instance classification via neural networks. Enhancing bag similarity techniques via inter-bag attention</b>. 
    <!-- <a href="https://proceedings.neurips.cc/paper/2021/file/10c272d06794d3e5785d5e7c5356e9ff-Paper.pdf" target="blank">[NeurIPS2021]</a> -->
</summary>

<!-- ```tex
@article{shao2021transmil,
  title={Transmil: Transformer based correlated multiple instance learning for whole slide image classification},
  author={Shao, Zhuchen and Bian, Hao and Chen, Yang and Wang, Yifeng and Zhang, Jian and Ji, Xiangyang and others},
  journal={Advances in Neural Information Processing Systems},
  volume={34},
  pages={2136--2147},
  year={2021}
}
``` -->

**Abstract:** The success of Multiple Instance Learning (MIL) has been confirmed by numerous studies and practical applications across various domains, including computer vision, biology, chemistry, medical diagnosis, and many others. Recently, leveraging deep neural networks to solve MIL problems has emerged as a successful approach. However, in most current multi-instance neural networks, the feature representation of each bag is learned individually, neglecting the relationships between bags. Therefore, this work introduces a novel neural network that emphasizes modeling the affinities between bags, capturing their similarity using attention mechanisms, thus achieving a richer and more effective bag representation compared to previous methods. The network, named Bag Attention Network (BAN), aims to outperform its pre-trained base model, used solely for bag embedding extraction. Experiments conducted on various MIL datasets demonstrate the performance comparison between the base model and BAN, showcasing the effectiveness of the latter.

</details>

![overview](img/ban_architecture.png)

## Installation

- Windows (Tested on Windows 11)
- CPU (Tested on CPU Intel Core i7 8th Gen)
- Python (3.7.16)

Please refer to the following instructions:

```bash
# create and activate the conda environment
conda create -n yourenvname python==3.7.16 -y
conda activate yourenvname
pip install -r requirements.txt
```

### Run

#### Run BAN on all datasets with all base models:
```python
run.bat #on Windows
./run.sh #on Linux
```

#### Run BAN with base model:
```python
python main_ban.py test_description --model=MI_net/attnet/sa_abmilp --dataset=musk1/musk2/elephant/fox/tiger/messidor
```

#### Run base model individually:
```python
python main.py test_description --model=MI_net/attnet/sa_abmilp --dataset=musk1/musk2/elephant/fox/tiger/messidor
```

<!-- #### mi-net (https://arxiv.org/abs/1610.02501):
```python
python main.py --model=minet --dataset=elephant
python main.py --model=minet --dataset=fox
python main.py --model=minet --dataset=tiger
python main.py --model=minet --dataset=musk1
python main.py --model=minet --dataset=musk2
python main.py --model=minet --dataset=messidor
```
#### MI-net (https://arxiv.org/abs/1610.02501):
```python
python main.py --model=MInet --dataset=elephant
python main.py --model=MInet --dataset=fox
python main.py --model=MInet --dataset=tiger
python main.py --model=MInet --dataset=musk1
python main.py --model=MInet --dataset=musk2
python main.py --model=MInet --dataset=messidor
```
#### Att-net (https://arxiv.org/abs/1802.04712):
```python
python main.py --model=attnet --dataset=elephant
python main.py --model=attnet --dataset=fox
python main.py --model=attnet --dataset=tiger
python main.py --model=attnet --dataset=musk1
python main.py --model=attnet --dataset=musk2
python main.py --model=attnet --dataset=messidor
``` -->
##### Default values:
```python
--run=5
--folds=10
--epochs=50
--no-cuda=False
--config=utils/settings.yaml #where you can change hyperparameteres
--eval-per-epoch=0 #Choose 0 if you do not want to save the best model, otherwise choose the number of times per epoch you want to save the best model (based on test set)
```

<!-- ### Test

```python
python train.py --stage='test' --config='Camelyon/TransMIL.yaml'  --gpus=0 --fold=0
```

## Reference

- If you found our work useful in your research, please consider citing our works(s) at:

```tex

@article{shao2021transmil,
  title={Transmil: Transformer based correlated multiple instance learning for whole slide image classification},
  author={Shao, Zhuchen and Bian, Hao and Chen, Yang and Wang, Yifeng and Zhang, Jian and Ji, Xiangyang and others},
  journal={Advances in Neural Information Processing Systems},
  volume={34},
  pages={2136--2147},
  year={2021}
}


```

© This code is made available under the GPLv3 License and is available for non-commercial academic purposes. -->
