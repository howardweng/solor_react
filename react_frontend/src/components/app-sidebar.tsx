"use client"

import * as React from "react"
import { useLocation } from "react-router-dom"

import { NavMain } from "@/components/nav-main"
import { NavProjects } from "@/components/nav-projects"
import { NavUser } from "@/components/nav-user"
import { TeamSwitcher } from "@/components/team-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"
import { getIcon } from "@/lib/icon-map"
import menuConfig from "@/config/sidebar-menu.json"

// User data (could also be moved to config or fetched from API)
const user = {
  name: "John Doe",
  email: "john@solarhub.com",
  avatar: "/avatar.png",
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const location = useLocation()

  // Transform teams with icons
  const teams = menuConfig.teams.map((team) => ({
    ...team,
    logo: getIcon(team.icon, team.iconColor),
  }))

  // Transform navMain with icons and active state
  const navMain = menuConfig.navMain.map((item) => ({
    ...item,
    icon: getIcon(item.icon, item.iconColor),
    isActive: location.pathname === item.url || location.pathname.startsWith(item.url + "/"),
  }))

  // Transform projects with icons
  const projects = menuConfig.projects.map((project) => ({
    ...project,
    icon: getIcon(project.icon, project.iconColor),
  }))

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={navMain} />
        <NavProjects projects={projects} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
