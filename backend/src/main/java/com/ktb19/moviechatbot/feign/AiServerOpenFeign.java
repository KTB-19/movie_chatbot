package com.ktb19.moviechatbot.feign;

import com.ktb19.moviechatbot.dto.AdditionalQueryRequest;
import com.ktb19.moviechatbot.dto.AiInfosResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient(name = "AiServer", url = "http://localhost:8000/api/v1")
public interface AiServerOpenFeign {

    @GetMapping("/infos")
    AiInfosResponse getInfos(@RequestParam String question);

    @PostMapping("/infos/additional")
    AiInfosResponse getInfosAdditional(@RequestBody AdditionalQueryRequest request);
}
