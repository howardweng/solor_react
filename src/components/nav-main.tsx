import { ChevronRight } from "lucide-react"
import { Link } from "react-router-dom"

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar"

// Type for 3-level nested navigation
type NavItem = {
  title: string
  url: string
  icon?: React.ReactNode
  isActive?: boolean
  items?: {
    title: string
    url: string
    items?: {
      title: string
      url: string
    }[]
  }[]
}

export function NavMain({
  items,
}: {
  items: NavItem[]
}) {
  return (
    <SidebarGroup>
      <SidebarGroupLabel>Main Menu</SidebarGroupLabel>
      <SidebarMenu>
        {items.map((item) =>
          item.items && item.items.length > 0 ? (
            <Collapsible
              key={item.title}
              asChild
              defaultOpen={item.isActive}
              className="group/collapsible"
            >
              <SidebarMenuItem>
                <CollapsibleTrigger asChild>
                  <SidebarMenuButton tooltip={item.title} isActive={item.isActive}>
                    {item.icon}
                    <span>{item.title}</span>
                    <span className="ml-auto flex items-center gap-1">
                      <span className="flex h-5 w-5 items-center justify-center rounded-full bg-gray-400 text-xs text-white">{item.items?.length}</span>
                      <ChevronRight className="transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
                    </span>
                  </SidebarMenuButton>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <SidebarMenuSub>
                    {item.items?.map((subItem) =>
                      subItem.items && subItem.items.length > 0 ? (
                        // Level 2 with children (Level 3)
                        <Collapsible
                          key={subItem.title}
                          asChild
                          className="group/collapsible-sub"
                        >
                          <SidebarMenuSubItem>
                            <CollapsibleTrigger asChild>
                              <SidebarMenuSubButton className="cursor-pointer">
                                <span>{subItem.title}</span>
                                <span className="ml-auto flex items-center gap-1">
                                  <span className="flex h-4 w-4 items-center justify-center rounded-full bg-gray-400 text-[10px] text-white">{subItem.items?.length}</span>
                                  <ChevronRight className="h-4 w-4 transition-transform duration-200 group-data-[state=open]/collapsible-sub:rotate-90" />
                                </span>
                              </SidebarMenuSubButton>
                            </CollapsibleTrigger>
                            <CollapsibleContent>
                              <SidebarMenuSub className="ml-2 border-l border-sidebar-border pl-2">
                                {subItem.items.map((thirdItem) => (
                                  <SidebarMenuSubItem key={thirdItem.title}>
                                    <SidebarMenuSubButton asChild>
                                      <Link to={thirdItem.url}>
                                        <span>{thirdItem.title}</span>
                                      </Link>
                                    </SidebarMenuSubButton>
                                  </SidebarMenuSubItem>
                                ))}
                              </SidebarMenuSub>
                            </CollapsibleContent>
                          </SidebarMenuSubItem>
                        </Collapsible>
                      ) : (
                        // Level 2 without children
                        <SidebarMenuSubItem key={subItem.title}>
                          <SidebarMenuSubButton asChild>
                            <Link to={subItem.url}>
                              <span>{subItem.title}</span>
                            </Link>
                          </SidebarMenuSubButton>
                        </SidebarMenuSubItem>
                      )
                    )}
                  </SidebarMenuSub>
                </CollapsibleContent>
              </SidebarMenuItem>
            </Collapsible>
          ) : (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton tooltip={item.title} isActive={item.isActive} asChild>
                <Link to={item.url}>
                  {item.icon}
                  <span>{item.title}</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          )
        )}
      </SidebarMenu>
    </SidebarGroup>
  )
}
