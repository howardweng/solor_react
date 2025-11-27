import { useState } from "react"
import {
  Sun,
  Zap,
  Battery,
  Gauge,
  MoreHorizontal,
  Search,
  Plus,
  RefreshCw,
  MapPin,
  Clock,
  Activity,
} from "lucide-react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Progress } from "@/components/ui/progress"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { solarDevices, type SolarDevice } from "@/lib/mock-data"

const deviceIcons = {
  panel: Sun,
  inverter: Zap,
  battery: Battery,
  meter: Gauge,
}

function DeviceCard({ device }: { device: SolarDevice }) {
  const Icon = deviceIcons[device.type]

  return (
    <Card className="group hover:shadow-lg transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div
              className={`p-2 rounded-lg ${
                device.status === "online"
                  ? "bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400"
                  : device.status === "warning"
                  ? "bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400"
                  : "bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-400"
              }`}
            >
              <Icon className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-base">{device.name}</CardTitle>
              <CardDescription>{device.id}</CardDescription>
            </div>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuItem>View Details</DropdownMenuItem>
              <DropdownMenuItem>View Analytics</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Configure</DropdownMenuItem>
              <DropdownMenuItem>Restart</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <Badge
            variant={
              device.status === "online"
                ? "default"
                : device.status === "warning"
                ? "secondary"
                : "destructive"
            }
          >
            {device.status}
          </Badge>
          <span className="text-sm capitalize text-muted-foreground">
            {device.type}
          </span>
        </div>

        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm">
            <MapPin className="h-4 w-4 text-muted-foreground" />
            <span>{device.location}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Clock className="h-4 w-4 text-muted-foreground" />
            <span>Last reading: {device.lastReading}</span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 pt-2 border-t">
          <div>
            <p className="text-xs text-muted-foreground">Power Output</p>
            <p className="text-lg font-semibold">{device.power} kW</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Efficiency</p>
            <div className="flex items-center gap-2">
              <Progress value={device.efficiency} className="flex-1 h-2" />
              <span className="text-sm font-medium">{device.efficiency}%</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default function DevicesPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [typeFilter, setTypeFilter] = useState<string>("all")
  const [statusFilter, setStatusFilter] = useState<string>("all")

  const filteredDevices = solarDevices.filter((device) => {
    const matchesSearch =
      device.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      device.id.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesType = typeFilter === "all" || device.type === typeFilter
    const matchesStatus = statusFilter === "all" || device.status === statusFilter
    return matchesSearch && matchesType && matchesStatus
  })

  const stats = {
    total: solarDevices.length,
    online: solarDevices.filter((d) => d.status === "online").length,
    warning: solarDevices.filter((d) => d.status === "warning").length,
    offline: solarDevices.filter((d) => d.status === "offline").length,
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Devices</h1>
          <p className="text-muted-foreground">
            Manage and monitor your solar devices
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button size="sm">
            <Plus className="h-4 w-4 mr-2" />
            Add Device
          </Button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Devices</p>
                <p className="text-2xl font-bold">{stats.total}</p>
              </div>
              <Activity className="h-8 w-8 text-muted-foreground" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Online</p>
                <p className="text-2xl font-bold text-green-600">{stats.online}</p>
              </div>
              <div className="h-8 w-8 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
                <div className="h-3 w-3 rounded-full bg-green-500" />
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Warning</p>
                <p className="text-2xl font-bold text-yellow-600">{stats.warning}</p>
              </div>
              <div className="h-8 w-8 rounded-full bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
                <div className="h-3 w-3 rounded-full bg-yellow-500" />
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Offline</p>
                <p className="text-2xl font-bold text-red-600">{stats.offline}</p>
              </div>
              <div className="h-8 w-8 rounded-full bg-red-100 dark:bg-red-900 flex items-center justify-center">
                <div className="h-3 w-3 rounded-full bg-red-500" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-4 sm:flex-row">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search devices..."
            className="pl-8"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <Select value={typeFilter} onValueChange={setTypeFilter}>
          <SelectTrigger className="w-full sm:w-[150px]">
            <SelectValue placeholder="Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Types</SelectItem>
            <SelectItem value="panel">Solar Panel</SelectItem>
            <SelectItem value="inverter">Inverter</SelectItem>
            <SelectItem value="battery">Battery</SelectItem>
            <SelectItem value="meter">Meter</SelectItem>
          </SelectContent>
        </Select>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-full sm:w-[150px]">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="online">Online</SelectItem>
            <SelectItem value="warning">Warning</SelectItem>
            <SelectItem value="offline">Offline</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Tabs for Card/Table View */}
      <Tabs defaultValue="cards" className="w-full">
        <TabsList>
          <TabsTrigger value="cards">Cards</TabsTrigger>
          <TabsTrigger value="table">Table</TabsTrigger>
        </TabsList>

        <TabsContent value="cards" className="mt-4">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {filteredDevices.map((device) => (
              <DeviceCard key={device.id} device={device} />
            ))}
          </div>
          {filteredDevices.length === 0 && (
            <div className="text-center py-12">
              <p className="text-muted-foreground">No devices found</p>
            </div>
          )}
        </TabsContent>

        <TabsContent value="table" className="mt-4">
          <Card>
            <CardContent className="pt-6">
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Device</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead className="hidden md:table-cell">Location</TableHead>
                      <TableHead className="hidden sm:table-cell">Last Reading</TableHead>
                      <TableHead className="text-right">Power</TableHead>
                      <TableHead className="text-right hidden lg:table-cell">Efficiency</TableHead>
                      <TableHead className="w-[50px]"></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredDevices.map((device) => {
                      const Icon = deviceIcons[device.type]
                      return (
                        <TableRow key={device.id}>
                          <TableCell>
                            <div className="flex items-center gap-3">
                              <Icon className="h-4 w-4 text-muted-foreground" />
                              <div>
                                <p className="font-medium">{device.name}</p>
                                <p className="text-xs text-muted-foreground">{device.id}</p>
                              </div>
                            </div>
                          </TableCell>
                          <TableCell className="capitalize">{device.type}</TableCell>
                          <TableCell>
                            <Badge
                              variant={
                                device.status === "online"
                                  ? "default"
                                  : device.status === "warning"
                                  ? "secondary"
                                  : "destructive"
                              }
                            >
                              {device.status}
                            </Badge>
                          </TableCell>
                          <TableCell className="hidden md:table-cell">{device.location}</TableCell>
                          <TableCell className="hidden sm:table-cell">{device.lastReading}</TableCell>
                          <TableCell className="text-right">{device.power} kW</TableCell>
                          <TableCell className="text-right hidden lg:table-cell">
                            {device.efficiency}%
                          </TableCell>
                          <TableCell>
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" size="icon" className="h-8 w-8">
                                  <MoreHorizontal className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end">
                                <DropdownMenuItem>View Details</DropdownMenuItem>
                                <DropdownMenuItem>Configure</DropdownMenuItem>
                                <DropdownMenuItem>Restart</DropdownMenuItem>
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
