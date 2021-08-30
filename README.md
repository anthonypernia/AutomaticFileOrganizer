### Automatic File Organizer

This script keeps watching a folder that the user established in CONFIG.JSON and is pending of all the files that pass through it to save them in subfolders filtered by type, can be Images , Audio, Videos.

The link is https://github.com/anthonyperniah/AutomaticFileOrganizer

It has a video if you want to see how it works [ --> Link](https://github.com/anthonyperniah/AutomaticFileOrganizer/blob/master/video_demo/code_demo_video.mp4?raw=true)

Is used the Watchdog library to keep watching the folder and capture the events on it. The filter that is used is with the RE library and regular expressions.

the config.json example is in the repository, you can edit if you require.

![config.json](https://github.com/anthonyperniah/AutomaticFileOrganizer/blob/master/img/config_example.png?raw=true "config.json")