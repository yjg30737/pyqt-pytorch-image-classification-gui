import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

classes = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']

# Define the model
class Net(nn.Module):
    def __init__(self, num_classes):
        super(Net, self).__init__()
        self.data_augmentation = nn.Sequential(
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.RandomAffine(degrees=0, translate=(0.1, 0.1))
        )
        self.model = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(0.2),
            nn.Flatten(),
            nn.Linear(64 * 22 * 22, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.data_augmentation(x)
        return self.model(x)


class ImagePredictor:
    def __init__(self, model_path):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.load_model(model_path)
        self.transform = self.load_transform()

    def load_model(self, model_path):
        model = Net(len(classes)).to(self.device)
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        return model

    def load_transform(self):
        img_height = 180
        img_width = 180
        transform = transforms.Compose([
            transforms.Lambda(lambda img: img.convert('RGB')),
            transforms.Resize((img_height, img_width)),
            transforms.ToTensor()
        ])
        return transform

    def get_image_from_url(self, image_url):
        import requests
        from PIL import Image
        from io import BytesIO

        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        return image

    def predict_image(self, image):
        image = self.transform(image)
        image = image.unsqueeze(0)
        image = image.to(self.device)
        #
        output = self.model(image)
        _, predicted = torch.max(output, 1)

        prob = F.softmax(output, dim=1)[0] * 100

        prob_res = round(prob[predicted[0]].item(), 2)

        return f'<span style="color: blue">Predicted: {classes[predicted[0]]}</span><br/>' \
               f'Percent: {prob_res}'

# pred = ImagePredictor('result.pth')
# image = pred.get_image_from_url('https://www.health.com/thmb/AADrlQdpWITCjFjKnfBnqWy5A8w=/2153x0/filters:no_upscale():max_bytes(150000):strip_icc()/Dandelion-d5aed7a95a6f4b16a3e954aa78694626.jpg')
# print(pred.predict_image(image))
# image = pred.get_image_from_url('https://ucarecdn.com/8b756a96-8495-4d00-9201-601d6b49c700/')
# print(pred.predict_image(image))
# image = pred.get_image_from_url('https://www.bolster.eu/media/images/5460_dbweb.jpg?1549350221')
# print(pred.predict_image(image))