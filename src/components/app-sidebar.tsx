"use client"

import * as React from "react"
import {
  Sun,
  LayoutDashboard,
  BarChart3,
  Zap,
  Battery,
  Settings2,
  Users,
  Bell,
} from "lucide-react"
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

// SolarHub data
const data = {
  user: {
    name: "John Doe",
    email: "john@solarhub.com",
    avatar: "/avatar.png",
  },
  teams: [
    {
      name: "SolarHub",
      logo: Sun,
      plan: "IoT Dashboard",
    },
  ],
  navMain: [
    {
      title: "Dashboard",
      url: "/dashboard",
      icon: LayoutDashboard,
      isActive: true,
    },
    {
      title: "Devices",
      url: "/devices",
      icon: Sun,
      items: [
        {
          title: "Solar Panels",
          url: "/devices/panels",
          items: [
            { title: "Panel A1", url: "/devices/panels/a1" },
            { title: "Panel A2", url: "/devices/panels/a2" },
            { title: "Panel B1", url: "/devices/panels/b1" },
          ],
        },
        {
          title: "Inverters",
          url: "/devices/inverters",
          items: [
            { title: "Main Inverter", url: "/devices/inverters/main" },
            { title: "Backup Inverter", url: "/devices/inverters/backup" },
          ],
        },
        {
          title: "Sensors",
          url: "/devices/sensors",
        },
      ],
    },
    {
      title: "Analytics",
      url: "/analytics",
      icon: BarChart3,
      items: [
        {
          title: "Reports",
          url: "/analytics/reports",
          items: [
            { title: "Daily Report", url: "/analytics/reports/daily" },
            { title: "Weekly Report", url: "/analytics/reports/weekly" },
            { title: "Monthly Report", url: "/analytics/reports/monthly" },
          ],
        },
        {
          title: "Charts",
          url: "/analytics/charts",
        },
        {
          title: "Export",
          url: "/analytics/export",
        },
      ],
    },
    {
      title: "Energy",
      url: "/energy",
      icon: Zap,
    },
    {
      title: "Battery",
      url: "/battery",
      icon: Battery,
    },
    {
      title: "Settings",
      url: "/settings",
      icon: Settings2,
      items: [
        {
          title: "General",
          url: "/settings",
        },
        {
          title: "Notifications",
          url: "/settings#notifications",
        },
        {
          title: "Security",
          url: "/settings#security",
        },
      ],
    },
  ],
  projects: [
    {
      name: "Users",
      url: "/users",
      icon: Users,
    },
    {
      name: "Alerts",
      url: "/alerts",
      icon: Bell,
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const location = useLocation()

  // Update isActive based on current route
  const navMainWithActive = data.navMain.map(item => ({
    ...item,
    isActive: location.pathname === item.url || location.pathname.startsWith(item.url + '/'),
  }))

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={navMainWithActive} />
        <NavProjects projects={data.projects} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
