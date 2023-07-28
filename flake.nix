{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system: let
      overlays = [ poetry2nix.overlay ];
      pkgs = import nixpkgs { inherit system overlays; };
    in {
      devShells.reroller = pkgs.mkShell {
        packages = with pkgs; [ git bashInteractive gcc meson ninja capnproto ];
      };
      devShells.sid2reroller = let
        env = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./sid2reroller;
          overrides = pkgs.poetry2nix.overrides.withDefaults (self: super: {
            pycapnp = super.pycapnp.overridePythonAttrs (old: {
              nativeBuildInputs = (old.nativeBuildInputs or []) ++ [
                self.setuptools
                self.pkgconfig
                self.python.pythonForBuild.pkgs.cython
              ];
              buildInputs = (old.buildInputs or []) ++ [ pkgs.capnproto ];
            });
          });
        };
      in pkgs.mkShell {
        packages = with pkgs; [ bashInteractive git env ];
      };

      apps.gen-dev-env = {
        type = "app";
        program = "${pkgs.writeScript "gen-dev-env.sh" ''
          #!/usr/bin/env bash

          # https://github.com/NixOS/nix/blob/a93110ab19085eeda1b4244fef49d18f91a1d7b8/src/nix/develop.cc#L257
          ignoreEnv=("BASHOPTS" "HOME" "NIX_BUILD_TOP" "NIX_ENFORCE_PURITY" "NIX_LOG_FD" "NIX_REMOTE" "PPID" "SHELL" "SHELLOPTS" "SSL_CERT_FILE" "TEMP" "TEMPDIR" "TERM" "TMP" "TMPDIR" "TZ" "UID")
          ignoreFilter=$(printf ",.key != \"%s\"" "''${ignoreEnv[@]}")

          nix print-dev-env --json $1 | ${pkgs.jq}/bin/jq -r "[.variables | to_entries | .[] | select(.value.type == \"exported\" and ([''${ignoreFilter:1}] | all)) | \"\(.key)=\" + @tsv \"\([.value.value])\"] | join(\"\n\")"
        ''}";
      };
    });
}
