// Simulated IoT Solar Data

export interface SolarDevice {
  id: string
  name: string
  type: "panel" | "inverter" | "battery" | "meter"
  status: "online" | "offline" | "warning"
  location: string
  lastReading: string
  power: number
  efficiency: number
}

export interface EnergyData {
  time: string
  production: number
  consumption: number
  gridExport: number
}

export interface BatteryData {
  id: string
  name: string
  capacity: number
  currentCharge: number
  status: "charging" | "discharging" | "idle"
  temperature: number
  health: number
}

export interface Alert {
  id: string
  type: "warning" | "error" | "info"
  message: string
  device: string
  timestamp: string
  acknowledged: boolean
}

// Dashboard Stats
export const dashboardStats = {
  totalProduction: 45.8,
  totalConsumption: 32.4,
  gridExport: 13.4,
  selfConsumption: 71,
  activePanels: 24,
  totalPanels: 28,
  batteryLevel: 78,
  co2Saved: 128.5,
}

// Solar Devices
export const solarDevices: SolarDevice[] = [
  {
    id: "SP-001",
    name: "Roof Array A",
    type: "panel",
    status: "online",
    location: "Building A - North",
    lastReading: "2 min ago",
    power: 4.2,
    efficiency: 94,
  },
  {
    id: "SP-002",
    name: "Roof Array B",
    type: "panel",
    status: "online",
    location: "Building A - South",
    lastReading: "1 min ago",
    power: 5.1,
    efficiency: 97,
  },
  {
    id: "SP-003",
    name: "Ground Mount 1",
    type: "panel",
    status: "warning",
    location: "Field Section 1",
    lastReading: "5 min ago",
    power: 2.8,
    efficiency: 72,
  },
  {
    id: "SP-004",
    name: "Ground Mount 2",
    type: "panel",
    status: "online",
    location: "Field Section 2",
    lastReading: "1 min ago",
    power: 4.9,
    efficiency: 95,
  },
  {
    id: "SP-005",
    name: "Carport Array",
    type: "panel",
    status: "online",
    location: "Parking Lot",
    lastReading: "3 min ago",
    power: 3.7,
    efficiency: 89,
  },
  {
    id: "SP-006",
    name: "Roof Array C",
    type: "panel",
    status: "offline",
    location: "Building B",
    lastReading: "2 hours ago",
    power: 0,
    efficiency: 0,
  },
  {
    id: "INV-001",
    name: "Main Inverter",
    type: "inverter",
    status: "online",
    location: "Equipment Room",
    lastReading: "1 min ago",
    power: 15.2,
    efficiency: 98,
  },
  {
    id: "INV-002",
    name: "Backup Inverter",
    type: "inverter",
    status: "online",
    location: "Equipment Room",
    lastReading: "1 min ago",
    power: 12.8,
    efficiency: 97,
  },
  {
    id: "BAT-001",
    name: "Battery Bank A",
    type: "battery",
    status: "online",
    location: "Storage Room",
    lastReading: "30 sec ago",
    power: 8.5,
    efficiency: 92,
  },
  {
    id: "MTR-001",
    name: "Grid Meter",
    type: "meter",
    status: "online",
    location: "Utility Room",
    lastReading: "10 sec ago",
    power: 13.4,
    efficiency: 100,
  },
]

// Energy production data (24 hours)
export const energyData: EnergyData[] = [
  { time: "00:00", production: 0, consumption: 2.1, gridExport: 0 },
  { time: "01:00", production: 0, consumption: 1.8, gridExport: 0 },
  { time: "02:00", production: 0, consumption: 1.5, gridExport: 0 },
  { time: "03:00", production: 0, consumption: 1.4, gridExport: 0 },
  { time: "04:00", production: 0, consumption: 1.6, gridExport: 0 },
  { time: "05:00", production: 0.5, consumption: 2.0, gridExport: 0 },
  { time: "06:00", production: 2.8, consumption: 3.2, gridExport: 0 },
  { time: "07:00", production: 8.5, consumption: 4.5, gridExport: 2.1 },
  { time: "08:00", production: 15.2, consumption: 5.8, gridExport: 6.4 },
  { time: "09:00", production: 22.5, consumption: 6.2, gridExport: 12.8 },
  { time: "10:00", production: 32.8, consumption: 7.1, gridExport: 18.5 },
  { time: "11:00", production: 38.5, consumption: 8.2, gridExport: 22.1 },
  { time: "12:00", production: 42.1, consumption: 9.5, gridExport: 24.5 },
  { time: "13:00", production: 45.8, consumption: 8.8, gridExport: 28.2 },
  { time: "14:00", production: 43.2, consumption: 7.5, gridExport: 26.8 },
  { time: "15:00", production: 38.6, consumption: 6.8, gridExport: 23.5 },
  { time: "16:00", production: 28.4, consumption: 7.2, gridExport: 15.2 },
  { time: "17:00", production: 18.5, consumption: 8.5, gridExport: 6.8 },
  { time: "18:00", production: 8.2, consumption: 9.2, gridExport: 0 },
  { time: "19:00", production: 2.1, consumption: 8.5, gridExport: 0 },
  { time: "20:00", production: 0, consumption: 6.8, gridExport: 0 },
  { time: "21:00", production: 0, consumption: 5.2, gridExport: 0 },
  { time: "22:00", production: 0, consumption: 3.8, gridExport: 0 },
  { time: "23:00", production: 0, consumption: 2.5, gridExport: 0 },
]

// Weekly production data
export const weeklyData = [
  { day: "Mon", production: 185, consumption: 142 },
  { day: "Tue", production: 210, consumption: 138 },
  { day: "Wed", production: 165, consumption: 145 },
  { day: "Thu", production: 198, consumption: 140 },
  { day: "Fri", production: 225, consumption: 152 },
  { day: "Sat", production: 195, consumption: 98 },
  { day: "Sun", production: 180, consumption: 85 },
]

// Monthly production data
export const monthlyData = [
  { month: "Jan", production: 2850, consumption: 3200 },
  { month: "Feb", production: 3100, consumption: 2900 },
  { month: "Mar", production: 4200, consumption: 2800 },
  { month: "Apr", production: 5100, consumption: 2600 },
  { month: "May", production: 5800, consumption: 2400 },
  { month: "Jun", production: 6200, consumption: 2500 },
  { month: "Jul", production: 6500, consumption: 2800 },
  { month: "Aug", production: 6100, consumption: 2900 },
  { month: "Sep", production: 5200, consumption: 2700 },
  { month: "Oct", production: 4100, consumption: 2800 },
  { month: "Nov", production: 3200, consumption: 3100 },
  { month: "Dec", production: 2600, consumption: 3400 },
]

// Battery data
export const batteryData: BatteryData[] = [
  {
    id: "BAT-001",
    name: "Battery Bank A",
    capacity: 50,
    currentCharge: 39,
    status: "charging",
    temperature: 28,
    health: 96,
  },
  {
    id: "BAT-002",
    name: "Battery Bank B",
    capacity: 50,
    currentCharge: 42,
    status: "idle",
    temperature: 26,
    health: 94,
  },
  {
    id: "BAT-003",
    name: "Battery Bank C",
    capacity: 25,
    currentCharge: 18,
    status: "discharging",
    temperature: 30,
    health: 89,
  },
]

// Alerts
export const alerts: Alert[] = [
  {
    id: "ALT-001",
    type: "warning",
    message: "Panel SP-003 efficiency dropped below 75%",
    device: "SP-003",
    timestamp: "10 min ago",
    acknowledged: false,
  },
  {
    id: "ALT-002",
    type: "error",
    message: "Panel SP-006 is offline - no communication",
    device: "SP-006",
    timestamp: "2 hours ago",
    acknowledged: false,
  },
  {
    id: "ALT-003",
    type: "info",
    message: "Battery Bank C temperature above optimal range",
    device: "BAT-003",
    timestamp: "1 hour ago",
    acknowledged: true,
  },
  {
    id: "ALT-004",
    type: "info",
    message: "Daily production target achieved",
    device: "System",
    timestamp: "3 hours ago",
    acknowledged: true,
  },
]

// Device type distribution for pie chart
export const deviceDistribution = [
  { type: "Solar Panels", count: 24, fill: "var(--chart-1)" },
  { type: "Inverters", count: 4, fill: "var(--chart-2)" },
  { type: "Batteries", count: 6, fill: "var(--chart-3)" },
  { type: "Meters", count: 3, fill: "var(--chart-4)" },
]

// Efficiency by location
export const locationEfficiency = [
  { location: "Building A", efficiency: 95 },
  { location: "Building B", efficiency: 45 },
  { location: "Field Section", efficiency: 84 },
  { location: "Parking Lot", efficiency: 89 },
]
