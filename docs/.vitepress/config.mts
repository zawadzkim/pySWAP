import { defineConfig, type DefaultTheme } from "vitepress";
import { createRequire } from "module";

const require = createRequire(import.meta.url);
const pkg = require("vitepress/package.json");

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "pySWAP",
  description: "python wrapper for SWAP model",
  base: "/pySWAP/",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: nav(),

    sidebar: {
      "/guide/": { base: "/guide/", items: sidebarGuide() },
      // '/reference/': { base: '/reference/', items: sidebarReference() }
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
      link: "/reference/api-reference",
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
      items: [
        { text: "Site Config", link: "site-config" },
        { text: "Frontmatter Config", link: "frontmatter-config" },
        { text: "Runtime API", link: "runtime-api" },
        { text: "CLI", link: "cli" },
        {
          text: "Default Theme",
          base: "/reference/default-theme-",
          items: [
            { text: "Overview", link: "config" },
            { text: "Nav", link: "nav" },
            { text: "Sidebar", link: "sidebar" },
            { text: "Home Page", link: "home-page" },
            { text: "Footer", link: "footer" },
            { text: "Layout", link: "layout" },
            { text: "Badge", link: "badge" },
            { text: "Team Page", link: "team-page" },
            { text: "Prev / Next Links", link: "prev-next-links" },
            { text: "Edit Link", link: "edit-link" },
            { text: "Last Updated Timestamp", link: "last-updated" },
            { text: "Search", link: "search" },
            { text: "Carbon Ads", link: "carbon-ads" },
          ],
        },
      ],
    },
  ];
}
