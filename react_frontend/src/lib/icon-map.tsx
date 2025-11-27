import DashboardIcon from "@mui/icons-material/Dashboard"
import WbSunnyIcon from "@mui/icons-material/WbSunny"
import BarChartIcon from "@mui/icons-material/BarChart"
import BoltIcon from "@mui/icons-material/Bolt"
import BatteryChargingFullIcon from "@mui/icons-material/BatteryChargingFull"
import SettingsIcon from "@mui/icons-material/Settings"
import PeopleIcon from "@mui/icons-material/People"
import NotificationsIcon from "@mui/icons-material/Notifications"
import HomeIcon from "@mui/icons-material/Home"
import DevicesIcon from "@mui/icons-material/Devices"
import AssessmentIcon from "@mui/icons-material/Assessment"
import SecurityIcon from "@mui/icons-material/Security"
import AccountCircleIcon from "@mui/icons-material/AccountCircle"
import HelpIcon from "@mui/icons-material/Help"
import InfoIcon from "@mui/icons-material/Info"
import BuildIcon from "@mui/icons-material/Build"
import StorageIcon from "@mui/icons-material/Storage"
import CloudIcon from "@mui/icons-material/Cloud"
import WifiIcon from "@mui/icons-material/Wifi"
import RouterIcon from "@mui/icons-material/Router"
import MemoryIcon from "@mui/icons-material/Memory"
import SpeedIcon from "@mui/icons-material/Speed"
import TrendingUpIcon from "@mui/icons-material/TrendingUp"
import PieChartIcon from "@mui/icons-material/PieChart"
import TimelineIcon from "@mui/icons-material/Timeline"
import ScheduleIcon from "@mui/icons-material/Schedule"
import CalendarTodayIcon from "@mui/icons-material/CalendarToday"
import FolderIcon from "@mui/icons-material/Folder"
import DescriptionIcon from "@mui/icons-material/Description"
import DownloadIcon from "@mui/icons-material/Download"
import UploadIcon from "@mui/icons-material/Upload"
import SyncIcon from "@mui/icons-material/Sync"
import PowerIcon from "@mui/icons-material/Power"
import FlashOnIcon from "@mui/icons-material/FlashOn"
import SolarPowerIcon from "@mui/icons-material/SolarPower"
import EnergySavingsLeafIcon from "@mui/icons-material/EnergySavingsLeaf"
import Inventory2Icon from "@mui/icons-material/Inventory2"
import LocalShippingIcon from "@mui/icons-material/LocalShipping"
import MapIcon from "@mui/icons-material/Map"
import LocationOnIcon from "@mui/icons-material/LocationOn"
import WarningIcon from "@mui/icons-material/Warning"
import ErrorIcon from "@mui/icons-material/Error"
import CheckCircleIcon from "@mui/icons-material/CheckCircle"
import type { SvgIconProps } from "@mui/material"

// Icon name to component mapping
const iconComponents: Record<string, React.ComponentType<SvgIconProps>> = {
  // Navigation & Dashboard
  dashboard: DashboardIcon,
  home: HomeIcon,

  // Solar & Energy
  sunny: WbSunnyIcon,
  solar_power: SolarPowerIcon,
  bolt: BoltIcon,
  flash_on: FlashOnIcon,
  power: PowerIcon,
  battery_charging_full: BatteryChargingFullIcon,
  energy_savings_leaf: EnergySavingsLeafIcon,

  // Analytics & Charts
  bar_chart: BarChartIcon,
  pie_chart: PieChartIcon,
  timeline: TimelineIcon,
  trending_up: TrendingUpIcon,
  assessment: AssessmentIcon,
  speed: SpeedIcon,

  // Devices & Hardware
  devices: DevicesIcon,
  memory: MemoryIcon,
  router: RouterIcon,
  wifi: WifiIcon,
  storage: StorageIcon,

  // Settings & Admin
  settings: SettingsIcon,
  build: BuildIcon,
  security: SecurityIcon,

  // Users & Notifications
  people: PeopleIcon,
  account_circle: AccountCircleIcon,
  notifications: NotificationsIcon,

  // Files & Data
  folder: FolderIcon,
  description: DescriptionIcon,
  download: DownloadIcon,
  upload: UploadIcon,
  sync: SyncIcon,
  cloud: CloudIcon,

  // Time & Schedule
  schedule: ScheduleIcon,
  calendar_today: CalendarTodayIcon,

  // Status
  warning: WarningIcon,
  error: ErrorIcon,
  check_circle: CheckCircleIcon,

  // Other
  help: HelpIcon,
  info: InfoIcon,
  inventory: Inventory2Icon,
  local_shipping: LocalShippingIcon,
  map: MapIcon,
  location_on: LocationOnIcon,
}

// Get icon component by name with color
export function getIcon(name: string, color?: string): React.ReactNode {
  const IconComponent = iconComponents[name]
  if (!IconComponent) {
    console.warn(`Icon "${name}" not found in icon map`)
    return null
  }
  return <IconComponent fontSize="small" sx={{ color: color || "inherit" }} />
}

// Export list of available icons for reference
export const availableIcons = Object.keys(iconComponents)
