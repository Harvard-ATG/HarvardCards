# -*- mode: ruby -*-
# vi: set ft=ruby :
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "hashicorp/precise64"
  #config.vm.host_name = "flashcards.fas.harvard.edu"
  config.vm.network :forwarded_port, guest: 8000, host: 8000, auto_correct: true

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "vagrant/manifests"
    puppet.manifest_file  = "default.pp"
  end

  config.vm.provider "virtualbox" do |v|
    # Seems to be required for Ubuntu
    # https://www.virtualbox.org/manual/ch03.html#settings-processor
    v.customize ["modifyvm", :id, "--pae", "on"]
    # Recommended for Ubuntu
    v.cpus = 2
    # This VM comes without swap memory enabled, so we need to bump up
    # from 512 in order to accomodate installation of lxml
    v.memory = 768
  end
  config.ssh.forward_agent = true

  # Add stdlib so we can use file_line module
  config.vm.provision :shell do |shell|
    shell.inline = "mkdir -p /etc/puppet/modules; puppet module install puppetlabs-stdlib --force;"
  end
end

