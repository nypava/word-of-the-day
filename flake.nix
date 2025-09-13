{
  description = "Word of the day";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = 
    {
    self,
    nixpkgs, 
    utils, 
    uv2nix,
    pyproject-nix,
    pyproject-build-systems,
    ...
    }:
    utils.lib.eachDefaultSystem (system: 
      let 
        inherit (nixpkgs) lib;
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python313;

        workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
        overlay = workspace.mkPyprojectOverlay {
          sourcePreference = "wheel"; 
        };

        pyprojectOverrides = _final: _prev: {
        };

        pythonSet =
          (pkgs.callPackage pyproject-nix.build.packages {
            inherit python;
          }).overrideScope
          (
            lib.composeManyExtensions [
              pyproject-build-systems.overlays.default
              overlay
              pyprojectOverrides
            ]
          );
      in {
        devShells = {
          default = self.devShells."${system}".impure;
          impure = pkgs.mkShell {
            packages = [
              python
              pkgs.uv
              pkgs.just
              pkgs.imagemagick
              pkgs.noto-fonts
            ];
            env =
              {
                UV_PYTHON_DOWNLOADS = "never";
                UV_PYTHON = python.interpreter;
              }
              // lib.optionalAttrs pkgs.stdenv.isLinux {
                LD_LIBRARY_PATH = lib.makeLibraryPath pkgs.pythonManylinuxPackages.manylinux1;
              };
            shellHook = ''
              unset PYTHONPATH
              '';
          };
          uv2nix =
            let
              # Create an overlay enabling editable mode for all local dependencies.
              editableOverlay = workspace.mkEditablePyprojectOverlay {
                # Use environment variable
                root = "$REPO_ROOT";
                # Optional: Only enable editable for these packages
                # members = [ "hello-world" ];
              };

              # Override previous set with our overrideable overlay.
              editablePythonSet = pythonSet.overrideScope editableOverlay;

              # Build virtual environment, with local packages being editable.
              #
              # Enable all optional dependencies for development.
              virtualenv = editablePythonSet.mkVirtualEnv "wordoftheday-dev-env" workspace.deps.all;

            in
              pkgs.mkShell {
                packages = [
                  virtualenv
                  pkgs.uv
                  pkgs.just
                ];

                env = {
                  # Don't create venv using uv
                  UV_NO_SYNC = "1";

                  # Force uv to use Python interpreter from venv
                  UV_PYTHON = "${virtualenv}/bin/python";

                  # Prevent uv from downloading managed Python's
                  UV_PYTHON_DOWNLOADS = "never";
                };

                shellHook = ''
                unset PYTHONPATH

                export REPO_ROOT=$(git rev-parse --show-toplevel)
                '';
              };
        };
      }
    );
}
