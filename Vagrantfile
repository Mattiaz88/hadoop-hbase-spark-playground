# -*- mode: ruby -*-
# vi: set ft=ruby :
 
# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.
 
  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty64"
 
  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64"
 
  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  #config.vm.network :forwarded_port, guest: 80, host: 8080
  #config.vm.network :forwarded_port, guest: 15672, host: 15672
  #config.vm.network :forwarded_port, guest: 5672, host: 5672
  #config.vm.network :forwarded_port, guest: 5432, host: 5432
 
  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network :private_network, ip: "192.168.33.11"
  
  config.vm.provider :virtualbox do |vb|      
    vb.customize ['modifyvm', :id, '--memory', 3000, '--cpus', 2]
  end
  
  config.vm.provision "setup",type: "fabric" do |fabric|
	fabric.fabric_path = "fab -D"
	fabric.fabfile_path = "./fabfile.py"
	fabric.tasks = ["provision", ]
  end
end