package main

import (
	"fmt"
	"goaqiagent/agent"
	"goaqiagent/api"
	"os"
	"strings"
)

func main() {

	if len(os.Args) < 3 {
		fmt.Println("Usage: go run main.go <state> <country>")
		return
	}

	state := os.Args[1]
	country := os.Args[2]

	apiKey := os.Getenv("GOOGLE_API_KEY")
	if apiKey == "" {
		fmt.Println("GOOGLE_API_KEY not set")
		return
	}

	lat, lng, err := api.GetCoordinates(state, country, apiKey)
	if err != nil {
		fmt.Println("Error getting coordinates:", err)
		return
	}

	aqi, err := api.GetAQI(lat, lng, apiKey)
	if err != nil {
		fmt.Println("Error getting AQI:", err)
		return
	}

	decision := agent.Agent(aqi)

	fmt.Printf("Latitude: %.4f | Longitude: %.4f\n", lat, lng)
	fmt.Printf("AQI: %d\n", aqi)
	fmt.Println("Decision:", decision)
}
