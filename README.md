# pyqt-pytorch-image-classification-gui
<div align="center">
  <img src="https://user-images.githubusercontent.com/55078043/229002952-9afe57de-b0b6-400f-9628-b8e0044d3f7b.png" width="150px" height="150px"><br/><br/>
  
  [![](https://dcbadge.vercel.app/api/server/cHekprskVE)](https://discord.gg/cHekprskVE)
</div>

PyQt5 usecase of pytorch image classification

This is the showcase of using a simple model that distinguishes between five types of flowers <b>(tulips, dandelions, sunflowers, daisies, and roses)</b> and presented result in a PyQt5 GUI.

The model training code can be found at <a href="https://www.kaggle.com/code/yoonjunggyu/pytorch-image-classification">kaggle notebook</a>.

The dataset includes five types of flowers, and the model was trained on this dataset for 15 epochs, with data augmentation applied to enhance accuracy.

The total size of the model file is small, at 15MB.

Below is a graph showing the changes in the model's performance (predictions, errors) according to the frequency of model training.

![image](https://github.com/yjg30737/pyqt-pytorch-image-classification-gui/assets/55078043/44df6e02-b0d8-4b8d-87a0-ea77fc0167ae)

It can be seen that the model's performance gradually improves as it trains.

If you are interested in learning about basic AI model creation with PyTorch, obtaining datasets, training methods, and utilization, please refer <a href="https://github.com/yjg30737/pyqt-torch-cnn-cifar10-gui.git">here</a>!

## How to Run
1. git clone ~
2. python main.py

## Preview
![image](https://github.com/yjg30737/pyqt-pytorch-image-classification-gui/assets/55078043/434dbff1-e56d-491b-9fc2-49df07f14f44)
