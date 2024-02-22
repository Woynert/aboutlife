{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
	name = "dev-environment";
	buildInputs = [
		pkgs.git
		pkgs.python3
		pkgs.gtk3
		pkgs.python311Packages.pygobject3
        pkgs.python311Packages.tornado
        pkgs.gobject-introspection

        pkgs.vte
        pkgs.libgudev
        pkgs.pcre2

        pkgs.meson
        pkgs.ninja
        pkgs.pkg-config
        pkgs.wrapGAppsHook
        pkgs.ruff
	];
	shellHook = ''
		echo "Starting development shell"

		# custom prompt
		if [ -e ~/.gitconfig ] && [ -f ~/.git-prompt.sh ]; then
			source ~/.git-prompt.sh
			PS1='\[\033[01;33m\]nix:\w\[\033[01;34m\]$(__git_ps1 " %s")\[\033[33m\]\$\[\033[00m\] '
		fi
	'';
}

