#!/bin/bash
echo "Mac OSX Only!"
echo "Please input your password to allow for installation"
echo "NOTE: No charecters will appear as you type, its still working"
#Install dependencies:
#ffmpeg
#lame
#youtube-dl
#id3tag
sudo echo "Starting installation"
echo "Installing dependencies..."
#Here lets make the directories we need
if [ -d /usr/local ]; then
:
else
sudo mkdir /usr/local
fi
if [ -d /usr/local/bin ]; then
:
else
sudo mkdir /usr/local/bin
fi
if [ -d /usr/local/lib ]; then
:
else
sudo mkdir /usr/local/lib
fi
if [ -d ~/Downloads/Song\ Downloader\ 1.0.0 ]; then
directory=~/Downloads/Song\ Downloader\ 1.0.0
else
directory=`find ~ -name "Song Downloader 1.0.0" -maxdepth 3`
fi
cd "$directory"
cd "Song Downloader"
cd Dependencies
sudo cp -R binFiles/* /usr/local/bin
sudo cp -R libFiles/* /usr/local/lib
cd ..
echo "Finishing up"
#Installation of our files
mkdir ~/Library/Application\ Support/Song\ Downloader
sudo mv "Download Song List.command" ~/Desktop
mkdir ~/Music/YoutubeSongs
cd ..
#Curr directory is the very top
cp -R Song\ Downloader/* ~/Library/Application\ Support/Song\ Downloader/
cd ~/Desktop &> /dev/null
echo "Song Name : Artist Name" > "Songs To Be Downloaded.txt" 
echo "Installation complete"
