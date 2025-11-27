
import { useState } from "react"
import {
  TrendingUp,
  TrendingDown,
  Calendar,
  Download,
  ArrowUpRight,
} from "lucide-react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart"
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  Line,
  LineChart,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  RadialBarChart,
  RadialBar,
} from "recharts"
import { energyData, weeklyData, monthlyData, locationEfficiency } from "@/lib/mock-data"

const chartConfig = {
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

const efficiencyData = locationEfficiency.map((item) => ({
  ...item,
  fill:
    item.efficiency > 90
      ? "var(--chart-1)"
      : item.efficiency > 70
      ? "var(--chart-2)"
      : "var(--chart-5)",
}))

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState("week")

  // Calculate totals
  const totalProduction = monthlyData.reduce((sum, d) => sum + d.production, 0)
  const totalConsumption = monthlyData.reduce((sum, d) => sum + d.consumption, 0)
  const netEnergy = totalProduction - totalConsumption
  const efficiency = Math.round((totalProduction / (totalProduction + 5000)) * 100)

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Analytics</h1>
          <p className="text-muted-foreground">
            Detailed insights and performance metrics
          </p>
        </div>
        <div className="flex gap-2">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-[140px]">
              <Calendar className="h-4 w-4 mr-2" />
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="day">Today</SelectItem>
              <SelectItem value="week">This Week</SelectItem>
              <SelectItem value="month">This Month</SelectItem>
              <SelectItem value="year">This Year</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid gap-4 grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Total Production</CardDescription>
            <CardTitle className="text-2xl md:text-3xl">
              {(totalProduction / 1000).toFixed(1)} MWh
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center text-sm text-green-600">
              <TrendingUp className="h-4 w-4 mr-1" />
              +15.2% from last year
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Total Consumption</CardDescription>
            <CardTitle className="text-2xl md:text-3xl">
              {(totalConsumption / 1000).toFixed(1)} MWh
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center text-sm text-red-600">
              <TrendingDown className="h-4 w-4 mr-1" />
              -3.8% from last year
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Net Energy</CardDescription>
            <CardTitle className="text-2xl md:text-3xl text-green-600">
              +{(netEnergy / 1000).toFixed(1)} MWh
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center text-sm text-muted-foreground">
              <ArrowUpRight className="h-4 w-4 mr-1" />
              Exported to grid
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>System Efficiency</CardDescription>
            <CardTitle className="text-2xl md:text-3xl">{efficiency}%</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center text-sm text-green-600">
              <TrendingUp className="h-4 w-4 mr-1" />
              +2.1% from last month
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Charts */}
      <Tabs defaultValue="production" className="space-y-4">
        <TabsList className="w-full sm:w-auto">
          <TabsTrigger value="production">Production</TabsTrigger>
          <TabsTrigger value="comparison">Comparison</TabsTrigger>
          <TabsTrigger value="efficiency">Efficiency</TabsTrigger>
        </TabsList>

        <TabsContent value="production" className="space-y-4">
          <div className="grid gap-4 lg:grid-cols-2">
            {/* Daily Energy Flow */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>Daily Energy Flow</CardTitle>
                <CardDescription>Production, consumption, and grid export over 24 hours</CardDescription>
              </CardHeader>
              <CardContent className="h-[350px]">
                <ChartContainer config={chartConfig} className="h-full w-full">
                  <LineChart data={energyData}>
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
                    <ChartLegend content={<ChartLegendContent />} />
                    <Line
                      type="monotone"
                      dataKey="production"
                      stroke="var(--chart-1)"
                      strokeWidth={2}
                      dot={false}
                    />
                    <Line
                      type="monotone"
                      dataKey="consumption"
                      stroke="var(--chart-2)"
                      strokeWidth={2}
                      dot={false}
                    />
                    <Line
                      type="monotone"
                      dataKey="gridExport"
                      stroke="var(--chart-3)"
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ChartContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="comparison" className="space-y-4">
          <div className="grid gap-4 lg:grid-cols-2">
            {/* Weekly Comparison */}
            <Card>
              <CardHeader>
                <CardTitle>Weekly Comparison</CardTitle>
                <CardDescription>Production vs consumption this week</CardDescription>
              </CardHeader>
              <CardContent className="h-[300px]">
                <ChartContainer config={chartConfig} className="h-full w-full">
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
                    <ChartLegend content={<ChartLegendContent />} />
                    <Bar dataKey="production" fill="var(--chart-1)" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="consumption" fill="var(--chart-2)" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ChartContainer>
              </CardContent>
            </Card>

            {/* Monthly Trends */}
            <Card>
              <CardHeader>
                <CardTitle>Monthly Trends</CardTitle>
                <CardDescription>Year-to-date energy data</CardDescription>
              </CardHeader>
              <CardContent className="h-[300px]">
                <ChartContainer config={chartConfig} className="h-full w-full">
                  <AreaChart data={monthlyData}>
                    <defs>
                      <linearGradient id="fillProd" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="var(--chart-1)" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="var(--chart-1)" stopOpacity={0.1} />
                      </linearGradient>
                      <linearGradient id="fillCons" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="var(--chart-2)" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="var(--chart-2)" stopOpacity={0.1} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis
                      dataKey="month"
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
                    <Area
                      type="monotone"
                      dataKey="production"
                      stroke="var(--chart-1)"
                      fill="url(#fillProd)"
                      strokeWidth={2}
                    />
                    <Area
                      type="monotone"
                      dataKey="consumption"
                      stroke="var(--chart-2)"
                      fill="url(#fillCons)"
                      strokeWidth={2}
                    />
                  </AreaChart>
                </ChartContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="efficiency" className="space-y-4">
          <div className="grid gap-4 lg:grid-cols-2">
            {/* Location Efficiency */}
            <Card>
              <CardHeader>
                <CardTitle>Efficiency by Location</CardTitle>
                <CardDescription>Performance breakdown by installation site</CardDescription>
              </CardHeader>
              <CardContent className="h-[300px]">
                <ChartContainer config={chartConfig} className="h-full w-full">
                  <BarChart data={locationEfficiency} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                    <XAxis
                      type="number"
                      domain={[0, 100]}
                      tickLine={false}
                      axisLine={false}
                      tickFormatter={(value) => `${value}%`}
                    />
                    <YAxis
                      type="category"
                      dataKey="location"
                      tickLine={false}
                      axisLine={false}
                      width={100}
                    />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <Bar
                      dataKey="efficiency"
                      fill="var(--chart-1)"
                      radius={[0, 4, 4, 0]}
                    />
                  </BarChart>
                </ChartContainer>
              </CardContent>
            </Card>

            {/* Efficiency Radial */}
            <Card>
              <CardHeader>
                <CardTitle>Overall System Health</CardTitle>
                <CardDescription>Current efficiency metrics</CardDescription>
              </CardHeader>
              <CardContent className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <RadialBarChart
                    cx="50%"
                    cy="50%"
                    innerRadius="30%"
                    outerRadius="90%"
                    data={efficiencyData}
                    startAngle={180}
                    endAngle={0}
                  >
                    <RadialBar
                      dataKey="efficiency"
                      cornerRadius={10}
                      background
                    />
                    <ChartTooltip />
                  </RadialBarChart>
                </ResponsiveContainer>
                <div className="flex flex-wrap justify-center gap-4 mt-4">
                  {locationEfficiency.map((item) => (
                    <div key={item.location} className="flex items-center gap-2 text-sm">
                      <div
                        className={`h-3 w-3 rounded-full ${
                          item.efficiency > 90
                            ? "bg-[var(--chart-1)]"
                            : item.efficiency > 70
                            ? "bg-[var(--chart-2)]"
                            : "bg-[var(--chart-5)]"
                        }`}
                      />
                      <span>{item.location}: {item.efficiency}%</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Additional Insights */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Peak Production</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-primary">45.8 kW</div>
            <p className="text-sm text-muted-foreground mt-1">
              Today at 1:00 PM
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Self-Consumption Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">71%</div>
            <p className="text-sm text-muted-foreground mt-1">
              Of produced energy used on-site
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Grid Independence</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600">85%</div>
            <p className="text-sm text-muted-foreground mt-1">
              Energy from solar vs grid
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
