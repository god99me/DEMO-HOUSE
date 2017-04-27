package io.github.god99me.demo.greeting;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.atomic.AtomicLong;

/**
 * Created by L.M.Y on 2017/4/27.
 */
@RestController
public class GreetingController {

    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();

    @RequestMapping("/greeting")
    public Greeting greeting(@RequestParam(value = "name", defaultValue = "REST") String name) {
        return new Greeting(counter.incrementAndGet(), String.format(template, name));
    }
}

//    A key difference between a traditional MVC controller and the RESTful web service controller
//    above is the way that the HTTP response body is created. Rather than relying on a view technology
//    to perform server-side rendering of the greeting data to HTML
