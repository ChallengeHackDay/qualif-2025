FROM golang:1.22.1 AS golang-builder
WORKDIR /builder
COPY . .
RUN go get .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o /builder/main .

FROM alpine:3.20.3
RUN apk --no-cache add ca-certificates
WORKDIR /chall
COPY --from=golang-builder /builder/main /chall
RUN chmod +x /chall/main

ENTRYPOINT ["/chall/main"]