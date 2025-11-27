
import { useState } from "react"
import {
  AlertTriangle,
  AlertCircle,
  Info,
  CheckCircle,
  Filter,
  Bell,
  BellOff,
} from "lucide-react"
import {
  Card,
  CardContent,
} from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { alerts } from "@/lib/mock-data"

const alertIcons = {
  error: AlertCircle,
  warning: AlertTriangle,
  info: Info,
}

const alertColors = {
  error: "bg-red-50 border-red-200 dark:bg-red-950 dark:border-red-900",
  warning: "bg-yellow-50 border-yellow-200 dark:bg-yellow-950 dark:border-yellow-900",
  info: "bg-blue-50 border-blue-200 dark:bg-blue-950 dark:border-blue-900",
}

const iconColors = {
  error: "text-red-500",
  warning: "text-yellow-500",
  info: "text-blue-500",
}

export default function AlertsPage() {
  const [typeFilter, setTypeFilter] = useState<string>("all")
  const [showAcknowledged, setShowAcknowledged] = useState(true)

  const filteredAlerts = alerts.filter((alert) => {
    const matchesType = typeFilter === "all" || alert.type === typeFilter
    const matchesAck = showAcknowledged || !alert.acknowledged
    return matchesType && matchesAck
  })

  const unacknowledgedCount = alerts.filter((a) => !a.acknowledged).length
  const errorCount = alerts.filter((a) => a.type === "error").length
  const warningCount = alerts.filter((a) => a.type === "warning").length

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Alerts</h1>
          <p className="text-muted-foreground">
            System notifications and warnings
          </p>
        </div>
        <Button variant="outline">
          <CheckCircle className="h-4 w-4 mr-2" />
          Mark All Read
        </Button>
      </div>

      {/* Stats */}
      <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2">
              <Bell className="h-5 w-5 text-primary" />
              <div>
                <p className="text-sm text-muted-foreground">Unread</p>
                <p className="text-2xl font-bold">{unacknowledgedCount}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2">
              <AlertCircle className="h-5 w-5 text-red-500" />
              <div>
                <p className="text-sm text-muted-foreground">Errors</p>
                <p className="text-2xl font-bold text-red-600">{errorCount}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-yellow-500" />
              <div>
                <p className="text-sm text-muted-foreground">Warnings</p>
                <p className="text-2xl font-bold text-yellow-600">{warningCount}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2">
              <BellOff className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-sm text-muted-foreground">Resolved Today</p>
                <p className="text-2xl font-bold">12</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
        <Select value={typeFilter} onValueChange={setTypeFilter}>
          <SelectTrigger className="w-full sm:w-[150px]">
            <Filter className="h-4 w-4 mr-2" />
            <SelectValue placeholder="Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Types</SelectItem>
            <SelectItem value="error">Errors</SelectItem>
            <SelectItem value="warning">Warnings</SelectItem>
            <SelectItem value="info">Info</SelectItem>
          </SelectContent>
        </Select>
        <div className="flex items-center space-x-2">
          <Checkbox
            id="showAck"
            checked={showAcknowledged}
            onCheckedChange={(checked) => setShowAcknowledged(checked as boolean)}
          />
          <label htmlFor="showAck" className="text-sm">
            Show acknowledged alerts
          </label>
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {filteredAlerts.map((alert) => {
          const Icon = alertIcons[alert.type]
          return (
            <Card
              key={alert.id}
              className={`border-l-4 ${alertColors[alert.type]} ${
                alert.acknowledged ? "opacity-60" : ""
              }`}
            >
              <CardContent className="pt-6">
                <div className="flex items-start gap-4">
                  <div className={`mt-0.5 ${iconColors[alert.type]}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <p className="font-medium">{alert.message}</p>
                        <div className="flex flex-wrap items-center gap-2 mt-2 text-sm text-muted-foreground">
                          <Badge variant="outline">{alert.device}</Badge>
                          <span>•</span>
                          <span>{alert.timestamp}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {!alert.acknowledged && (
                          <div className="h-2 w-2 rounded-full bg-primary" />
                        )}
                        <Button variant="ghost" size="sm">
                          {alert.acknowledged ? "Reopen" : "Acknowledge"}
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )
        })}

        {filteredAlerts.length === 0 && (
          <Card>
            <CardContent className="py-12 text-center">
              <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
              <p className="text-lg font-medium">All Clear!</p>
              <p className="text-muted-foreground">
                No alerts matching your filters
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
