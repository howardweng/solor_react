import {
  Sun,
  Zap,
  Battery,
  Leaf,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  ArrowUpRight,
  ArrowDownRight,
} from "lucide-react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  dashboardStats,
  energyData,
  weeklyData,
  solarDevices,
  alerts,
  deviceDistribution,
  batteryData,
} from "@/lib/mock-data"

const energyChartConfig = {
  production: {
    label: "Production",
    color: "var(--chart-1)",
  },
  consumption: {
    label: "Consumption",
    color: "var(--chart-2)",
  },
  gridExport: {
    label: "Grid Export",
    color: "var(--chart-3)",
  },
} satisfies ChartConfig

const weeklyChartConfig = {
  production: {
    label: "Production",
    color: "var(--chart-1)",
  },
  consumption: {
    label: "Consumption",
    color: "var(--chart-2)",
  },
} satisfies ChartConfig

export default function DashboardPage() {
  const activeDevices = solarDevices.filter((d) => d.status === "online").length
  const warningDevices = solarDevices.filter((d) => d.status === "warning").length
  const offlineDevices = solarDevices.filter((d) => d.status === "offline").length

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Real-time overview of your solar energy system
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Production</CardTitle>
            <Sun className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats.totalProduction} kWh</div>
            <p className="text-xs text-muted-foreground flex items-center gap-1">
              <TrendingUp className="h-3 w-3 text-green-500" />
              +12% from yesterday
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Consumption</CardTitle>
            <Zap className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats.totalConsumption} kWh</div>
            <p className="text-xs text-muted-foreground flex items-center gap-1">
              <TrendingDown className="h-3 w-3 text-green-500" />
              -5% from yesterday
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Battery Level</CardTitle>
            <Battery className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats.batteryLevel}%</div>
            <Progress value={dashboardStats.batteryLevel} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">CO2 Saved</CardTitle>
            <Leaf className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats.co2Saved} kg</div>
            <p className="text-xs text-muted-foreground">This month</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid gap-4 lg:grid-cols-7">
        {/* Energy Production Chart - Large */}
        <Card className="lg:col-span-4">
          <CardHeader>
            <CardTitle>Energy Overview</CardTitle>
            <CardDescription>Today's production vs consumption</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ChartContainer config={energyChartConfig} className="h-full w-full">
              <AreaChart data={energyData}>
                <defs>
                  <linearGradient id="fillProduction" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--chart-1)" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="var(--chart-1)" stopOpacity={0.1} />
                  </linearGradient>
                  <linearGradient id="fillConsumption" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--chart-2)" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="var(--chart-2)" stopOpacity={0.1} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis
                  dataKey="time"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  fontSize={12}
                />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  fontSize={12}
                  tickFormatter={(value) => `${value}kW`}
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Area
                  type="monotone"
                  dataKey="production"
                  stroke="var(--chart-1)"
                  fill="url(#fillProduction)"
                  strokeWidth={2}
                />
                <Area
                  type="monotone"
                  dataKey="consumption"
                  stroke="var(--chart-2)"
                  fill="url(#fillConsumption)"
                  strokeWidth={2}
                />
              </AreaChart>
            </ChartContainer>
          </CardContent>
        </Card>

        {/* Weekly Chart */}
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle>Weekly Comparison</CardTitle>
            <CardDescription>Production vs Consumption (kWh)</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ChartContainer config={weeklyChartConfig} className="h-full w-full">
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis
                  dataKey="day"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  fontSize={12}
                />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  fontSize={12}
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Bar dataKey="production" fill="var(--chart-1)" radius={[4, 4, 0, 0]} />
                <Bar dataKey="consumption" fill="var(--chart-2)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ChartContainer>
          </CardContent>
        </Card>
      </div>

      {/* Second Row - Status and Alerts */}
      <div className="grid gap-4 lg:grid-cols-3">
        {/* Device Status */}
        <Card>
          <CardHeader>
            <CardTitle>Device Status</CardTitle>
            <CardDescription>Real-time device monitoring</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-green-500" />
                  <span className="text-sm">Online</span>
                </div>
                <span className="font-bold">{activeDevices}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-yellow-500" />
                  <span className="text-sm">Warning</span>
                </div>
                <span className="font-bold">{warningDevices}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-red-500" />
                  <span className="text-sm">Offline</span>
                </div>
                <span className="font-bold">{offlineDevices}</span>
              </div>

              <div className="pt-4 border-t">
                <div className="text-sm text-muted-foreground mb-2">Device Distribution</div>
                <div className="h-[150px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={deviceDistribution}
                        dataKey="count"
                        nameKey="type"
                        cx="50%"
                        cy="50%"
                        innerRadius={40}
                        outerRadius={60}
                      >
                        {deviceDistribution.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.fill} />
                        ))}
                      </Pie>
                      <ChartTooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Battery Status */}
        <Card>
          <CardHeader>
            <CardTitle>Battery Banks</CardTitle>
            <CardDescription>Storage system status</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {batteryData.map((battery) => (
                <div key={battery.id} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Battery
                        className={`h-4 w-4 ${
                          battery.status === "charging"
                            ? "text-green-500"
                            : battery.status === "discharging"
                            ? "text-orange-500"
                            : "text-muted-foreground"
                        }`}
                      />
                      <span className="text-sm font-medium">{battery.name}</span>
                    </div>
                    <Badge
                      variant={
                        battery.status === "charging"
                          ? "default"
                          : battery.status === "discharging"
                          ? "secondary"
                          : "outline"
                      }
                    >
                      {battery.status}
                    </Badge>
                  </div>
                  <div className="flex items-center gap-2">
                    <Progress
                      value={(battery.currentCharge / battery.capacity) * 100}
                      className="flex-1"
                    />
                    <span className="text-sm text-muted-foreground w-16 text-right">
                      {battery.currentCharge}/{battery.capacity} kWh
                    </span>
                  </div>
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>Temp: {battery.temperature}°C</span>
                    <span>Health: {battery.health}%</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Alerts */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-yellow-500" />
              Recent Alerts
            </CardTitle>
            <CardDescription>System notifications</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {alerts.slice(0, 4).map((alert) => (
                <div
                  key={alert.id}
                  className={`p-3 rounded-lg border ${
                    alert.type === "error"
                      ? "bg-red-50 border-red-200 dark:bg-red-950 dark:border-red-900"
                      : alert.type === "warning"
                      ? "bg-yellow-50 border-yellow-200 dark:bg-yellow-950 dark:border-yellow-900"
                      : "bg-blue-50 border-blue-200 dark:bg-blue-950 dark:border-blue-900"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1">
                      <p className="text-sm font-medium">{alert.message}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {alert.device} • {alert.timestamp}
                      </p>
                    </div>
                    {!alert.acknowledged && (
                      <div className="h-2 w-2 rounded-full bg-primary" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Devices Table */}
      <Card>
        <CardHeader>
          <CardTitle>Active Devices</CardTitle>
          <CardDescription>Real-time status of all solar devices</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Device</TableHead>
                  <TableHead className="hidden sm:table-cell">Type</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="hidden md:table-cell">Location</TableHead>
                  <TableHead className="text-right">Power</TableHead>
                  <TableHead className="hidden lg:table-cell text-right">Efficiency</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {solarDevices.slice(0, 6).map((device) => (
                  <TableRow key={device.id}>
                    <TableCell>
                      <div>
                        <p className="font-medium">{device.name}</p>
                        <p className="text-xs text-muted-foreground">{device.id}</p>
                      </div>
                    </TableCell>
                    <TableCell className="hidden sm:table-cell capitalize">
                      {device.type}
                    </TableCell>
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
                    <TableCell className="text-right">{device.power} kW</TableCell>
                    <TableCell className="hidden lg:table-cell text-right">
                      <div className="flex items-center justify-end gap-2">
                        <span>{device.efficiency}%</span>
                        {device.efficiency > 90 ? (
                          <ArrowUpRight className="h-4 w-4 text-green-500" />
                        ) : device.efficiency > 0 ? (
                          <ArrowDownRight className="h-4 w-4 text-red-500" />
                        ) : null}
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
