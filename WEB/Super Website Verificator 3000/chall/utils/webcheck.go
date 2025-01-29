package utils

import (
	"fmt"
	"io"
	"net/http"
	"regexp"
	"time"
)

func Check(url string) (body string, fetchTime string, hasMetaTag bool, err error) {
	start := time.Now()

	client := http.Client{
		Timeout: 3 * time.Second,
	}
	resp, err := client.Get(url)
	duration := time.Since(start)
	fetchTime = fmt.Sprintf("%v", duration)
	if err != nil {
		return
	}
	defer resp.Body.Close()

	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return
	}

	body = string(bodyBytes)

	metaRegex := regexp.MustCompile(`<\s*meta\s.*(name|property)=['"](og:)?(description|robots|rating|tags)['"]`)
	hasMetaTag = metaRegex.MatchString(body)
	return
}
