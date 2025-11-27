
import {
  Zap,
  TrendingUp,
  TrendingDown,
  ArrowRightLeft,
  Gauge,
} from "lucide-react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { Area, AreaChart, XAxis, YAxis, CartesianGrid } from "recharts"
import { energyData } from "@/lib/mock-data"

const chartConfig = {
  production: {
    label: "Production",
    color: "var(--chart-1)",
  },
  consumption: {
    label: "Consumption",
    color: "var(--chart-2)",
  },
} satisfies ChartConfig

export default function EnergyPage() {
  const currentProduction = 38.5
  const currentConsumption = 24.2
  const gridFlow = currentProduction - currentConsumption

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Energy Flow</h1>
        <p className="text-muted-foreground">
          Real-time energy production and consumption monitoring
        </p>
      </div>

      {/* Real-time Stats */}
      <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="border-l-4 border-l-primary">
          <CardHeader className="pb-2">
            <CardDescription className="flex items-center gap-2">
              <Zap className="h-4 w-4" />
              Current Production
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{currentProduction} kW</div>
            <div className="flex items-center text-sm text-green-600 mt-1">
              <TrendingUp className="h-4 w-4 mr-1" />
              +5.2% from peak
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-orange-500">
          <CardHeader className="pb-2">
            <CardDescription className="flex items-center gap-2">
              <Gauge className="h-4 w-4" />
              Current Consumption
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{currentConsumption} kW</div>
            <div className="flex items-center text-sm text-muted-foreground mt-1">
              <TrendingDown className="h-4 w-4 mr-1" />
              Normal range
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-green-500">
          <CardHeader className="pb-2">
            <CardDescription className="flex items-center gap-2">
              <ArrowRightLeft className="h-4 w-4" />
              Grid Export
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600">+{gridFlow.toFixed(1)} kW</div>
            <p className="text-sm text-muted-foreground mt-1">Exporting to grid</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Self-Consumption</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">63%</div>
            <Progress value={63} className="mt-2" />
          </CardContent>
        </Card>
      </div>

      {/* Energy Flow Diagram */}
      <Card>
        <CardHeader>
          <CardTitle>Energy Flow Diagram</CardTitle>
          <CardDescription>Visual representation of energy distribution</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row items-center justify-center gap-8 py-8">
            {/* Solar */}
            <div className="text-center">
              <div className="w-24 h-24 md:w-32 md:h-32 rounded-full bg-primary/20 flex items-center justify-center mx-auto mb-2">
                <div className="w-16 h-16 md:w-20 md:h-20 rounded-full bg-primary flex items-center justify-center text-primary-foreground">
                  <Zap className="h-8 w-8 md:h-10 md:w-10" />
                </div>
              </div>
              <p className="font-medium">Solar Production</p>
              <p className="text-2xl font-bold text-primary">{currentProduction} kW</p>
            </div>

            {/* Arrow */}
            <div className="hidden md:flex items-center">
              <div className="w-16 h-1 bg-primary" />
              <div className="w-0 h-0 border-t-8 border-t-transparent border-b-8 border-b-transparent border-l-8 border-l-primary" />
            </div>

            {/* Home */}
            <div className="text-center">
              <div className="w-24 h-24 md:w-32 md:h-32 rounded-full bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center mx-auto mb-2">
                <div className="w-16 h-16 md:w-20 md:h-20 rounded-full bg-orange-500 flex items-center justify-center text-white">
                  <Gauge className="h-8 w-8 md:h-10 md:w-10" />
                </div>
              </div>
              <p className="font-medium">Home Usage</p>
              <p className="text-2xl font-bold text-orange-600">{currentConsumption} kW</p>
            </div>

            {/* Arrow */}
            <div className="hidden md:flex items-center">
              <div className="w-16 h-1 bg-green-500" />
              <div className="w-0 h-0 border-t-8 border-t-transparent border-b-8 border-b-transparent border-l-8 border-l-green-500" />
            </div>

            {/* Grid */}
            <div className="text-center">
              <div className="w-24 h-24 md:w-32 md:h-32 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center mx-auto mb-2">
                <div className="w-16 h-16 md:w-20 md:h-20 rounded-full bg-green-500 flex items-center justify-center text-white">
                  <ArrowRightLeft className="h-8 w-8 md:h-10 md:w-10" />
                </div>
              </div>
              <p className="font-medium">Grid Export</p>
              <p className="text-2xl font-bold text-green-600">+{gridFlow.toFixed(1)} kW</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Today's Energy Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Today&apos;s Energy Pattern</CardTitle>
          <CardDescription>Production vs consumption over 24 hours</CardDescription>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ChartContainer config={chartConfig} className="h-full w-full">
            <AreaChart data={energyData}>
              <defs>
                <linearGradient id="prodGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--chart-1)" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="var(--chart-1)" stopOpacity={0.1} />
                </linearGradient>
                <linearGradient id="consGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--chart-2)" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="var(--chart-2)" stopOpacity={0.1} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="time" tickLine={false} axisLine={false} fontSize={12} />
              <YAxis tickLine={false} axisLine={false} fontSize={12} tickFormatter={(v) => `${v}kW`} />
              <ChartTooltip content={<ChartTooltipContent />} />
              <Area
                type="monotone"
                dataKey="production"
                stroke="var(--chart-1)"
                fill="url(#prodGrad)"
                strokeWidth={2}
              />
              <Area
                type="monotone"
                dataKey="consumption"
                stroke="var(--chart-2)"
                fill="url(#consGrad)"
                strokeWidth={2}
              />
            </AreaChart>
          </ChartContainer>
        </CardContent>
      </Card>
    </div>
  )
}
