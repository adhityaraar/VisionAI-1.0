# VisionAI
VisionAI is a project that uses object detection to detect personal protective equipment (PPE) in a given image. The project is built using the YOLOv5 model and is deployed on a Jetson Nano device. The project is built using Python and Flask.

![alt text](ppe.png)
![alt text](videoconstruction.gif)

## There are 3 steps to run the VisionAI project:

### Jetson Nano Preparation 
• Prepare your Jetson Nano, camera device, and support device 

• Installation: 
    jetpack==4.6.1 
    Ubuntu==18.04 
    cuda==10.2 
    Python==3.8.18

### Setup Python Virtual Environment 
To run the code in your local, it is best to setup a virtual environment first. 

• Create new environment using conda in local: 
    conda create --name VisionAI --file requirements.txt 
    conda activate VisionAI 

• if using Jetson nano, need to install manually from libraries by using bash .sh 
    `sudo bash installPython.sh sh`
    `sudo bash enlargeMemorySwap.sh sh`
    `sudo bash pre_installOpencv.sh sh`
    `sudo bash installOpencvandtorch.sh sh`

### Running object detection 
Run the VisionAI object detection. Here, we are using flask bash python app.py

Access it on other device (local network    )
• make sure the device have one internet connection, check the local ip address: 
    `ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}'`
• The example result will be, url=192.xx.xx.xx
• Run in your browser device: `http://:5000/`