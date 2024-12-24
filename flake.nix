{
  description = "A flake for a Python development environment with requests package";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    {
      devShells.default = nixpkgs.lib.mkShell {
        packages = with nixpkgs; [
          python310
          (python310Packages.requests) # Add the requests package
        ];
      };
    };
}
