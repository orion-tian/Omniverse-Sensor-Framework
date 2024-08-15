# Omniverse Sensor Framework
Nvidia Omniverse extension proof of concept to visualize real-time sensor data to work towards creating a digital twin in Omniverse.

<img width="468" alt="Picture1" src="https://github.com/user-attachments/assets/eaf19c70-1c77-4c53-b92d-596a9cbcb62a">

To use this extension, you will first select the mesh you want to place the sensor in and specify the sensor Id of the sensor through the drop down menu. Then, you click the Create Sensor button, and a sphere mesh is created at the center of the selected mesh’s bounding box. In addition, a UI element is drawn on top of the sphere so the location of the sensor can be easily seen no matter where the sensor or the viewport is. 

The UI element can also have gestures, the human-input system of Omniverse, attached to it, meaning it can react to mouse clicks and keyboard presses. Currently, we have a click gesture attached so that when you click on the UI element, a pop-up window shows up with a graph of the sensor’s temperature data, which is currently read from a csv file we wrote. You can also adjust the position of the sphere mesh to better reflect the real world position of the sensor and the UI element will follow.

The eventual goal of this framework is that the sensor’s data will drive the color of the mesh it’s associated with. Possibly using attributes and time sampling in order for colors to change in real-time when you press play in Omniverse. We also envision how this extension could draw data from the cloud to get real-time data. In fact, this system is highly extensible to other fields such as representing strain sensors on elevators or sensors at a construction site.

__________________________________________________________________________________________________________________________________________________________________________________________________________________________

# Extension Project Template

This project was automatically generated.

- `app` - It is a folder link to the location of your *Omniverse Kit* based app.
- `exts` - It is a folder where you can add new extensions. It was automatically added to extension search path. (Extension Manager -> Gear Icon -> Extension Search Path).

Open this folder using Visual Studio Code. It will suggest you to install few extensions that will make python experience better.

Look for "orion.sensor" extension in extension manager and enable it. Try applying changes to any python files, it will hot-reload and you can observe results immediately.

Alternatively, you can launch your app from console with this folder added to search path and your extension enabled, e.g.:

```
> app\omni.code.bat --ext-folder exts --enable omni.hello.world
```

# App Link Setup

If `app` folder link doesn't exist or broken it can be created again. For better developer experience it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. Convenience script to use is included.

Run:

```
> link_app.bat
```

If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```
> link_app.bat --app create
```

You can also just pass a path to create link to:

```
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2021.3.4"
```


# Sharing Your Extensions

This folder is ready to be pushed to any git repository. Once pushed direct link to a git repository can be added to *Omniverse Kit* extension search paths.

Link might look like this: `git://github.com/[user]/[your_repo].git?branch=main&dir=exts`

Notice `exts` is repo subfolder with extensions. More information can be found in "Git URL as Extension Search Paths" section of developers manual.

To add a link to your *Omniverse Kit* based app go into: Extension Manager -> Gear Icon -> Extension Search Path

