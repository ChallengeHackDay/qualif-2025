package utils

import (
	"fmt"
	"net"
	"net/url"
	"regexp"
)

func ValidateURL(input string) error {
	parsedURL, err := url.Parse(input)
	if err != nil {
		return fmt.Errorf("invalid URL")
	}

	// Check if the scheme is http or https
	if parsedURL.Scheme != "http" && parsedURL.Scheme != "https" {
		return fmt.Errorf("invalid scheme : use http or https")
	}

	// Check if the host is a valid domain name
	domainRegex := regexp.MustCompile(`^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$`)
	if !domainRegex.MatchString(parsedURL.Hostname()) {
		return fmt.Errorf("you must provide a valid domain name")
	}

	// Check if the host isn't an IP address
	ipRegex := regexp.MustCompile(`^((?:25[0-5]|2[0-4]\d|[0-1]?\d{1,2})(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d{1,2})){3})|(([[:xdigit:]]{1,4}(?::[[:xdigit:]]{1,4}){7}|::|:(?::[[:xdigit:]]{1,4}){1,6}|[[:xdigit:]]{1,4}:(?::[[:xdigit:]]{1,4}){1,5}|(?:[[:xdigit:]]{1,4}:){2}(?::[[:xdigit:]]{1,4}){1,4}|(?:[[:xdigit:]]{1,4}:){3}(?::[[:xdigit:]]{1,4}){1,3}|(?:[[:xdigit:]]{1,4}:){4}(?::[[:xdigit:]]{1,4}){1,2}|(?:[[:xdigit:]]{1,4}:){5}:[[:xdigit:]]{1,4}|(?:[[:xdigit:]]{1,4}:){1,6}:))$`)
	if ipRegex.MatchString(parsedURL.Hostname()) {
		return fmt.Errorf("ip adresses are not allowed")
	}

	// Check if the domain is resolvable
	ips, err := net.LookupIP(parsedURL.Hostname())
	if err != nil || len(ips) == 0 {
		return fmt.Errorf("could not resolve the domain")
	}

	// Check if the domain is not pointing at localhost
	for _, ip := range ips {
		if ip.IsLoopback() || ip.IsLinkLocalUnicast() || ip.IsLinkLocalMulticast() || ip.IsPrivate() {
			return fmt.Errorf("localhost and resolved private addresse aren't allowed (resolved IP: %s)", ip.String())
		}
	}

	return nil
}
