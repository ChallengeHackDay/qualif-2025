package main

import (
	"embed"
	"fmt"
	"net/http"
	"os"
	"websitecheckup/handlers"

	"github.com/charmbracelet/log"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

//go:embed public
var publicFS embed.FS

func main() {

	listenPort := os.Getenv("LISTEN_PORT")
	if listenPort == "" {
		log.Fatal("LISTEN_PORT is not set")
	}

	e := echo.New()
	e.HideBanner = true

	e.Use(middleware.StaticWithConfig(middleware.StaticConfig{
		Root:       "public",
		Filesystem: http.FS(publicFS),
	}))

	api := e.Group("/api")
	api.POST("/check", handlers.Check)

	// Start internal server
	go func() {
		internalPort := os.Getenv("INTERNAL_PORT")
		if internalPort == "" {
			log.Fatal("INTERNAL_PORT is not set")
		}

		flag := os.Getenv("FLAG")
		if flag == "" {
			log.Fatal("FLAG is not set")
		}

		internal := echo.New()
		internal.HideBanner = true
		internal.GET("/", func(c echo.Context) error {
			return c.String(http.StatusOK, fmt.Sprintf("How did you find this? Here is your flag: %s", flag))
		})
		internal.Start(":" + internalPort)
	}()

	err := e.Start(":" + listenPort)
	if err != nil {
		log.Fatal("Router handler stopped", "error", err)
	}
}
