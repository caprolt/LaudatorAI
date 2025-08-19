import * as React from "react"
import { cn } from "@/lib/utils"

interface ElegantCardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'gold' | 'maroon' | 'transparent'
  glow?: boolean
}

const ElegantCard = React.forwardRef<HTMLDivElement, ElegantCardProps>(
  ({ className, variant = 'default', glow = false, ...props }, ref) => {
    const variantClasses = {
      default: "bg-white/95 backdrop-blur-sm border border-yellow-400/20",
      gold: "bg-gradient-to-br from-yellow-50 to-yellow-100/50 border border-yellow-400/40",
      maroon: "bg-gradient-to-br from-red-50 to-red-100/50 border border-red-400/40",
      transparent: "bg-white/10 backdrop-blur-sm border border-yellow-400/30"
    }

    const glowClasses = glow ? "gold-shadow" : "shadow-lg"

    return (
      <div
        ref={ref}
        className={cn(
          "rounded-xl border bg-card text-card-foreground transition-all duration-300",
          variantClasses[variant],
          glowClasses,
          className
        )}
        {...props}
      />
    )
  }
)
ElegantCard.displayName = "ElegantCard"

const ElegantCardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
ElegantCardHeader.displayName = "ElegantCardHeader"

const ElegantCardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-xl font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
))
ElegantCardTitle.displayName = "ElegantCardTitle"

const ElegantCardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
ElegantCardDescription.displayName = "ElegantCardDescription"

const ElegantCardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
ElegantCardContent.displayName = "ElegantCardContent"

const ElegantCardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
ElegantCardFooter.displayName = "ElegantCardFooter"

export { 
  ElegantCard, 
  ElegantCardHeader, 
  ElegantCardFooter, 
  ElegantCardTitle, 
  ElegantCardDescription, 
  ElegantCardContent 
}
