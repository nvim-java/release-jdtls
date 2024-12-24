# :coffee: mason-registry

![Neovim](https://img.shields.io/badge/NeoVim-%2357A143.svg?&style=for-the-badge&logo=neovim&logoColor=white)
![Lua](https://img.shields.io/badge/lua-%232C2D72.svg?style=for-the-badge&logo=lua&logoColor=white)
![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=openjdk&logoColor=white)
![Gradle](https://img.shields.io/badge/Gradle-02303A.svg?style=for-the-badge&logo=Gradle&logoColor=white)
![Apache Maven](https://img.shields.io/badge/Apache%20Maven-C71A36?style=for-the-badge&logo=Apache%20Maven&logoColor=white)

This project daily checks new JDTLS versions and re-package new versions without timestamps in the package and equinox launcher

Related issues:

- https://github.com/mason-org/mason-registry/issues/8073
- https://github.com/mason-org/mason-registry/issues/5788
- https://github.com/mason-org/mason-registry/issues/3017

## How to Install

- You can add the new registry before the default mason-registry as follows
- Run `Mason` and wait for mason to update the new registry

```lua
{
  'williamboman/mason.nvim',
  opts = {
    registries = {
      'github:nvim-java/mason-registry',
      'github:mason-org/mason-registry',
    },
  },
}
```

## Head on to main project [:coffee: nvim-java](https://github.com/nvim-java/nvim-java)
