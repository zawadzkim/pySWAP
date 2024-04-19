import { defineConfig, type DefaultTheme } from "vitepress";
import { createRequire } from "module";

const require = createRequire(import.meta.url);
const pkg = require("vitepress/package.json");

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: " ",
  description: "python wrapper for SWAP model",
  base: "/pySWAP/",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: "/logo.webp",
    nav: nav(),

    sidebar: {
      "/guide/": { base: "/guide/", items: sidebarGuide() },
      "/reference/": { base: "/reference/", items: sidebarReference() },
    },

    socialLinks: [
      { icon: "github", link: "https://github.com/zawadzkim/pySWAP" },
    ],
    footer: {
      message: "Released under the MIT License.",
      copyright: "Copyright © 2024 Mateusz Zawadzki",
    },
  },
});

function nav(): DefaultTheme.NavItem[] {
  return [
    {
      text: "Guide",
      link: "/guide/what-is-pyswap",
      activeMatch: "/guide/",
    },
    {
      text: "Reference",
      link: "/reference/api-reference.md",
      activeMatch: "/reference/",
    },
    {
      text: pkg.version,
      items: [
        {
          text: "Changelog",
          link: "https://github.com/zawadzkim/pySWAP/blob/main/docs/CHANGELOG.md",
        },
        {
          text: "Contributing",
          link: "https://github.com/zawadzkim/pySWAP/blob/main/.github/CONTRIBUTING.md",
        },
      ],
    },
  ];
}

function sidebarGuide(): DefaultTheme.SidebarItem[] {
  return [
    {
      text: "Introduction",
      collapsed: false,
      items: [
        { text: "What is pySWAP?", link: "what-is-pyswap" },
        { text: "Getting Started", link: "getting-started" },
        { text: "Generic classes", link: "generic-classes" },
        { text: "Model class", link: "model-class" },
      ],
    },
    {
      text: "Preparing SWAP input",
      collapsed: false,
      items: [
        { text: "Main swp settings", link: "swp-module" },
        { text: "Meteorological data", link: "met-module" },
        { text: "Crop modules", link: "crp-module" },
        { text: "Drainage", link: "dra-module" },
        { text: "Irrigation", link: "irg-modeule" },
      ],
    },
  ];
}

function sidebarReference(): DefaultTheme.SidebarItem[] {
  return [
    {
      text: "Reference",
      items: [{ text: "API reference", link: "api-reference" }],
    },
  ];
}
