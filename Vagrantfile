# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|

  config.vm.provider :virtualbox do |v|
    v.memory = "4096"
    v.gui = false
  end
  # config.vm.box = "geerlingguy/ubuntu1604"
  config.vm.box = "ubuntu/trusty64"
   config.vm.synced_folder '.', '/vagrant', nfs: true

# Configure vagrant-cachier plugin
if Vagrant.has_plugin?("vagrant-cachier")
    # Configure cached packages to be shared between instances of the same base box.
    # More info on http://fgrehm.viewdocs.io/vagrant-cachier/usage
    config.cache.scope = :machine

    # OPTIONAL: If you are using VirtualBox, you might want to use that to enable
    # NFS for shared folders. This is also very useful for vagrant-libvirt if you
    # want bi-directional sync
    config.cache.synced_folder_opts = {
      type: :nfs,
    # The nolock option can be useful for an NFSv3 client that wants to avoid the
    # NLM sideband protocol. Without this option, apt-get might hang if it tries
    # to lock files needed for /var/cache/* operations. All of this can be avoided
    # by using NFSv4 everywhere. Please note that the tcp option is not the default.
    mount_options: ['rw', 'vers=3', 'tcp', 'nolock']
    }
    # For more information please check http://docs.vagrantup.com/v2/synced-folders/basic_usage.html
    end
    # @end: Configure vagrant-cachier plugin
    # Configure vagrant-cachier plugin
    if Vagrant.has_plugin?("vagrant-hostmanager")
      config.hostmanager.enabled = true
      config.hostmanager.manage_host = true
      config.hostmanager.ignore_private_ip = false
      config.hostmanager.include_offline = true
    end
    # @end: Configure vagrant-cachier plugin
    config.vm.define "py3netudev" do |py3netudev|
      py3netudev.vm.host_name = "py3netudev"
      py3netudev.vm.network :private_network, ip: "192.168.82.131"
       py3netudev.vm.network :forwarded_port,
        guest: 3000,
        host: 3000,
        auto_correct: true
      py3netudev.ssh.forward_agent = true
      py3netudev.vm.provision "ansible" do |ansible|
          ansible.verbose = "v"
          ansible.playbook = "ansible/sites.yml"
      end
  end
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL
end
