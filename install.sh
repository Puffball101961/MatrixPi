#!/bin/bash

# Clear the terminal
clear

# Check for root
if [ "$(id -u)" != "0" ]; then
    echo "Please run this script as root. Exiting..."
    exit 1
fi

if [[ $1 != "--resume" ]]; then
    
    # Display ASCII art
    echo """
    ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗██████╗ ██╗
    ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝██╔══██╗██║
    ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝ ██████╔╝██║
    ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ ██╔═══╝ ██║
    ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗██║     ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
    made by Joel @ puffball.dev

    This is Open source software, covered by the GPLv3 License.

    """
    echo "You're about to install MatrixPi."

    read -p "Do you want to proceed? [y/N] " response
    case "$response" in
        y|Y )
        echo "Preparing..."
        clear

        # Update and upgrade and install git
        echo "Step 1: apt-get update and upgrade, install git"
        sleep 1
        apt-get update && apt-get upgrade -y
        apt-get install git -y
        echo "Done."
        sleep 1
        clear

        # Clone the repository
        echo "Step 2: Downloading MatrixPi"
        sleep 1
        git clone --depth=1 --branch=wip https://github.com/Puffball101961/MatrixPi.git /home/pi/MatrixPi
        chown -R pi:pi /home/pi/MatrixPi
        echo "Done."
        sleep 1
        clear

        # Copy all system services
        echo "Step 3: Copying system services"
        sleep 1
        cp /home/pi/MatrixPi/services/* /etc/systemd/system/
        echo "Done."
        sleep 1
        clear

        # Configure automatic system updates/upgrades
        echo "Step 4: Configuring automatic system updates/upgrades"
        echo "Would you like to enable automatic system updates/upgrades? (Strongly Recommended)"
        read -p "Do you want to enable? [Y/n] " response
        case "$response" in
            n|N ) 
            echo "Leaving automatic system updates/upgrades disabled."
            echo "You will be responsible for manually updating/upgrading your system."
            sleep 1
            clear
            ;;
            * )
            echo "Enabling automatic system updates/upgrades."
            sleep 1
            apt-get install unattended-upgrades -y
            echo "Done."
            sleep 1
            clear
            ;;
        esac

        # Install all dependencies
        echo "Step 5: Install dependencies"
        echo "This step may take a while depending on your Raspberry Pi model and SD card performance."
        sleep 1
        apt-get install python3 python3-dev python3-pillow python3-pip cython3 -y
        python -m venv ./MatrixPi/env
        sudo ./MatrixPi/env/bin/pip install -r ./MatrixPi/requirements.txt
        git clone https://github.com/hzeller/rpi-rgb-led-matrix --depth=1
        ( cd ./rpi-rgb-led-matrix ; make build-python PYTHON=/home/pi/MatrixPi/env/bin/python3 )
        ( cd ./rpi-rgb-led-matrix ; sudo make install-python PYTHON=/home/pi/MatrixPi/env/bin/python3 )
        echo "Done."
        sleep 1
        clear

        # Configure Raspberry Pi OS
        echo "Step 6: Making tweaks to RPi OS"
        sleep 1

        echo "Have you run this script before on this Pi? If so, running the following step again may cause issues. Please skip this step if you have already run through this step."
        read -p "Skip OS Tweaks? (y/N)" response
        case "$response" in
            y|Y )  
            echo "Skipping OS Tweaks"
            sleep 1
            clear
            ;;
            * )
            echo "Expanding Root Filesystem"
            raspi-config nonint do_expand_rootfs
            echo "Isolating CPU core for display"
            cat /boot/firmware/cmdline.txt | grep -q isolcpus=3 || sed -i -e 's/$/ isolcpus=3/' /boot/firmware/cmdline.txt
            echo "Blacklisting audio module"
            sudo rm /etc/modprobe.d/blacklist-rgb-matrix.conf
            echo "blacklist snd_bcm2835" | sudo tee /etc/modprobe.d/blacklist-rgb-matrix.conf
            update-initramfs -u
            echo "Done."
            echo "You now need to reboot to continue to the next step of the installation."
            echo "When you are back to the command line, run "sudo install.sh --resume" to continue."
            read -r -p "Press enter to reboot now."
            sudo reboot
            sleep 2
            ;;
        esac
        ;;
        * )
        echo "Installation aborted. Exiting..."
        exit 1
        
    esac
fi

# Configure matrix parameters
echo "Step 7: Configure matrix parameters"
sleep 1
read -p "What is the total width in pixels of your matrix? " cols
read -p "What is the total height in pixels of your matrix? " rows
echo -e "\nGreat! Your matrix is $cols x $rows pixels in size."
sleep 1
clear

# Check display mapping
echo "Step 8a: Check display hardware mapping"
echo "A test pattern will be shown on the matrix display in a few seconds."
sleep 1
( cd ./MatrixPi/setup ; /home/pi/MatrixPi/env/bin/python ./checkHardwareMapping.py --led-no-hardware-pulse $rows $cols adafruit-hat-pwm)
read -r -p "Did you see MatrixPi on your matrix display? [y/N] " response
case "$response" in
    y|Y ) 
    echo "Great. Your hardware should be fully supported."
    ;;
    * )
    echo "Your hardware may not be fully supported or may be broken. Installation will not continue."
    exit 1
    ;;
esac
read -r -p "Was the text the correct way up (not upside down) [Y/n] " response
case "$response" in
    n|N )
    echo "No rotation required"
    rotation=0
    ;;
    * )
    echo "Display is going to be rotated 180 degrees"
    rotation=1
    ;;
esac

sleep 1
clear

# Check colour mapping
echo "Step 8b: Check display colour mapping"
echo "Another test pattern will be shown on the matrix display in a few seconds."
sleep 1
( cd ./MatrixPi/setup ; /home/pi/MatrixPi/env/bin/python ./checkColourMapping.py --led-no-hardware-pulse $rows $cols adafruit-hat-pwm RBG)
read -r -p "Did you see the colours in the following order: RED, GREEN, BLUE? [Y/n]" response
case "$response" in
    n|N )
    echo "Great. Your colours are mapped correctly."
    colourMapping=RBG
    ;;
    * )
    echo "I've adjusted the colour mapping. Another test pattern will be displayed shortly."
    sleep 2
    ( cd ./MatrixPi/setup ; /home/pi/MatrixPi/env/bin/python3 ./checkColourMapping.py --no-led-hardware-pulse $rows $cols adafruit-hat-pwm RGB)
    read -r -p "Did you see the colours in the following order: RED, GREEN, BLUE? [Y/n]" response
    case "$response" in
        n|N )
        echo "Great. Your colours are mapped correctly."
        colourMapping=RGB
        ;;
        * )
        echo "Your colour mapping is not currently supported by the installer!" # TODO: Add more colour mapping options
        exit 1
        ;;
    esac
;;
esac

sleep 1
clear

echo "Please wait while your configuration is processed."
/home/pi/MatrixPi/env/bin/python3 ./MatrixPi/scripts/updateConfig.py $cols $rows adafruit-hat-pwm $colourMapping
sleep 1

echo "Configurations updated!"
sleep 1
clear

echo "Enabling MatrixPi system service"
sleep 1
sudo systemctl enable matrixpi

echo "Installation complete!"
echo "You must now reboot your Pi to fully install MatrixPi."
;;