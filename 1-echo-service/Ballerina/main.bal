import ballerina/http;

service / on new http:Listener(8090) {
    resource function post echo(@http:Payload string textMsg) returns string {
        return textMsg;
    }
    resource function get health() returns string {
        return "Service Running";
    }
}
