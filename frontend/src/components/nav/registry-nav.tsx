"use client"

import {
  BackToWorkspaceNavButton,
  IntegrationsNavButton,
  OrganizationNavButton,
  RegistryNavButton,
} from "@/components/nav/nav-buttons"

export function RegistryNav() {
  return (
    <nav className="flex space-x-4 lg:space-x-6">
      <BackToWorkspaceNavButton />
      <IntegrationsNavButton />
      <RegistryNavButton />
      <OrganizationNavButton />
    </nav>
  )
}
