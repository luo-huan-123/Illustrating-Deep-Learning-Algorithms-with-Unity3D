# Illustrating-Deep-Learning-Algorithms-with-Unity3D

This is a Pole Project in CentraleSupelec in which we want to design an interesting game which illustrates semantic segmentation algorithms using Unity 3D for those teenagers. The project has been finished by Songliang HAN, Yuqi Sun, Ping LIN, and Huan LUO. Jeremy Fix is our mentor.

## General information

Firstly, we have to download an indoor scene directly to our new Unity3D project. It looks like a perfect living-room. Then we insert turtlebot3 from ROS to Unity. (Tutorials [turtlebot2](https://github.com/siemens/ros-sharp/wiki/User_Inst_TurtleBot2), and[Transfer a URDF from ROS to Unity](https://github.com/siemens/ros-sharp/wiki/User_App_ROS_TransferURDFFromROS) are very useful.) You can download 'mygame' directly to complete the above steps. 

Next, we have to write a ROS package to communicate with Unity 3D. You could use our package named 'mycamera'. With the package, you could control the turtlebot3 in Unity 3D, subscribe the images captured by main camera in Unity, send them to dldemos server and recieve the semantic segmentation results. 

![image](https://github.com/luo-huan-123/Illustrating-Deep-Learning-Algorithms-with-Unity3D/main/Images/segmentation.jpg)
![image](https://github.com/luo-huan-123/Illustrating-Deep-Learning-Algorithms-with-Unity3D/main/Images/segmentation1.jpg)

## Steps 

To start with, we have to start the dldmos_sever. (you could follow this [tutorial](https://github.com/jeremyfix/deeplearning_demos)) Fortunately, we can use the CentraleSupelc’s GPU cluster. For connecting school’s GPU, you set the SSH key to avoid having to enter the password every connection, and book a machine, login and port forword(set up ssh tunnel). See details in [SSH](https://tutos.metz.centralesupelec.fr/TPs/SSH/), and [Book](https://tutos.metz.centralesupelec.fr/TPs/Clusters/allocation.html).  

Next, use 'UnityHub.AppImage' to open 'mygame'.

Then, you launch: 

    roslaunch mycamera webcam.launch
    
And start the game in Unity 3D.

Finally, you could enjoy the game. 




