package handlers

import (
	"net/http"
	"websitecheckup/utils"

	"github.com/labstack/echo/v4"
)

func Check(c echo.Context) error {

	url := c.FormValue("url")
	if url == "" {
		return c.JSON(http.StatusBadRequest, map[string]interface{}{
			"error": "url is required",
		})
	}

	if err := utils.ValidateURL(url); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]interface{}{
			"message": err.Error(),
		})
	}

	showBody := c.FormValue("showBody") == "on"

	body, fetchTime, hasMetaTag, err := utils.Check(url)
	if err != nil {
		return c.JSON(http.StatusOK, map[string]interface{}{
			"online": false,
		})
	}

	res := map[string]interface{}{
		"online":        true,
		"fetch_time":    fetchTime,
		"seo_meta_tags": hasMetaTag,
	}

	if showBody {
		res["body"] = body
	}

	return c.JSON(http.StatusOK, res)
}
