
"""
Builder class for LiveCD stage1.
"""

from generic_stage import *
import catalyst.util
from catalyst.spawn import cmd

class livecd_stage1_target(generic_stage_target):
	def __init__(self,spec,addlargs):
		self.required_values=["livecd/packages"]
		self.valid_values=self.required_values[:]

		self.valid_values.extend(["livecd/use"])
		generic_stage_target.__init__(self,spec,addlargs)

	def set_action_sequence(self):
		self.settings["action_sequence"]=["unpack","unpack_snapshot",\
					"config_profile_link","setup_confdir","portage_overlay",\
					"bind","chroot_setup","setup_environment","build_packages",\
					"unbind", "clean","clear_autoresume"]

	def set_target_path(self):
		self.settings["target_path"]=catalyst.util.normpath(self.settings["storedir"]+"/builds/"+self.settings["target_subpath"])
		if self.check_autoresume("setup_target_path"):
				print "Resume point detected, skipping target path setup operation..."
		else:
			# first clean up any existing target stuff
			if os.path.exists(self.settings["target_path"]):
				cmd("rm -rf "+self.settings["target_path"],\
					"Could not remove existing directory: "+self.settings["target_path"],env=self.env)
				self.set_autoresume("setup_target_path")

			if not os.path.exists(self.settings["target_path"]):
				os.makedirs(self.settings["target_path"])


	def set_target_path(self):
		pass

	def set_spec_prefix(self):
		self.settings["spec_prefix"]="livecd"

	def set_use(self):
		generic_stage_target.set_use(self)
		if "use" in self.settings:
			self.settings["use"].append("livecd")
			self.settings["use"].append("bindist")
		else:
			self.settings["use"]=["livecd"]
			self.settings["use"].append("bindist")

	def set_packages(self):
		generic_stage_target.set_packages(self)
		if self.settings["spec_prefix"]+"/packages" in self.settings:
			if type(self.settings[self.settings["spec_prefix"]+"/packages"]) == types.StringType:
				self.settings[self.settings["spec_prefix"]+"/packages"] = \
					self.settings[self.settings["spec_prefix"]+"/packages"].split()
		self.settings[self.settings["spec_prefix"]+"/packages"].append("app-misc/livecd-tools")

	def set_pkgcache_path(self):
		if "pkgcache_path" in self.settings:
			if type(self.settings["pkgcache_path"]) != types.StringType:
				self.settings["pkgcache_path"]=catalyst.util.normpath(string.join(self.settings["pkgcache_path"]))
		else:
			generic_stage_target.set_pkgcache_path(self)

__target_map = {"livecd-stage1":livecd_stage1_target}
