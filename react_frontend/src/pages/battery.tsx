
import {
  Battery,
  BatteryCharging,
  Thermometer,
  Heart,
  Zap,
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
import { Line, LineChart, XAxis, YAxis, CartesianGrid } from "recharts"
import { batteryData } from "@/lib/mock-data"

const chartConfig = {
  charge: {
    label: "Charge Level",
    color: "var(--chart-1)",
  },
} satisfies ChartConfig

// Simulated battery history data
const batteryHistory = [
  { time: "00:00", charge: 45 },
  { time: "04:00", charge: 35 },
  { time: "08:00", charge: 42 },
  { time: "12:00", charge: 78 },
  { time: "16:00", charge: 92 },
  { time: "20:00", charge: 85 },
  { time: "Now", charge: 78 },
]

export default function BatteryPage() {
  const totalCapacity = batteryData.reduce((sum, b) => sum + b.capacity, 0)
  const totalCharge = batteryData.reduce((sum, b) => sum + b.currentCharge, 0)
  const overallPercentage = Math.round((totalCharge / totalCapacity) * 100)
  const avgHealth = Math.round(
    batteryData.reduce((sum, b) => sum + b.health, 0) / batteryData.length
  )

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Battery Storage</h1>
        <p className="text-muted-foreground">
          Monitor and manage your battery bank systems
        </p>
      </div>

      {/* Overview Cards */}
      <div className="grid gap-4 grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardDescription className="flex items-center gap-2">
              <Battery className="h-4 w-4" />
              Total Capacity
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalCapacity} kWh</div>
            <p className="text-sm text-muted-foreground">
              Across {batteryData.length} banks
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardDescription className="flex items-center gap-2">
              <BatteryCharging className="h-4 w-4" />
              Current Charge
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalCharge} kWh</div>
            <Progress value={overallPercentage} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardDescription className="flex items-center gap-2">
              <Heart className="h-4 w-4" />
              Average Health
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{avgHealth}%</div>
            <p className="text-sm text-muted-foreground">Excellent condition</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardDescription className="flex items-center gap-2">
              <Zap className="h-4 w-4" />
              Power Flow
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">+4.2 kW</div>
            <p className="text-sm text-muted-foreground">Currently charging</p>
          </CardContent>
        </Card>
      </div>

      {/* Battery Banks */}
      <div className="grid gap-4 lg:grid-cols-3">
        {batteryData.map((battery) => (
          <Card key={battery.id}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className={`p-2 rounded-lg ${
                      battery.status === "charging"
                        ? "bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400"
                        : battery.status === "discharging"
                        ? "bg-orange-100 text-orange-600 dark:bg-orange-900 dark:text-orange-400"
                        : "bg-muted text-muted-foreground"
                    }`}
                  >
                    {battery.status === "charging" ? (
                      <BatteryCharging className="h-5 w-5" />
                    ) : (
                      <Battery className="h-5 w-5" />
                    )}
                  </div>
                  <div>
                    <CardTitle className="text-base">{battery.name}</CardTitle>
                    <CardDescription>{battery.id}</CardDescription>
                  </div>
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
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Charge Level */}
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Charge Level</span>
                  <span className="font-medium">
                    {battery.currentCharge}/{battery.capacity} kWh
                  </span>
                </div>
                <Progress
                  value={(battery.currentCharge / battery.capacity) * 100}
                />
                <p className="text-xs text-muted-foreground mt-1">
                  {Math.round((battery.currentCharge / battery.capacity) * 100)}% charged
                </p>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                <div className="flex items-center gap-2">
                  <Thermometer className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="text-xs text-muted-foreground">Temperature</p>
                    <p className="font-medium">{battery.temperature}°C</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Heart className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="text-xs text-muted-foreground">Health</p>
                    <p className="font-medium">{battery.health}%</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charge History Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Charge Level History</CardTitle>
          <CardDescription>Overall battery bank charge level today</CardDescription>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ChartContainer config={chartConfig} className="h-full w-full">
            <LineChart data={batteryHistory}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="time" tickLine={false} axisLine={false} fontSize={12} />
              <YAxis
                tickLine={false}
                axisLine={false}
                fontSize={12}
                domain={[0, 100]}
                tickFormatter={(v) => `${v}%`}
              />
              <ChartTooltip content={<ChartTooltipContent />} />
              <Line
                type="monotone"
                dataKey="charge"
                stroke="var(--chart-1)"
                strokeWidth={2}
                dot={{ fill: "var(--chart-1)", r: 4 }}
              />
            </LineChart>
          </ChartContainer>
        </CardContent>
      </Card>
    </div>
  )
}
