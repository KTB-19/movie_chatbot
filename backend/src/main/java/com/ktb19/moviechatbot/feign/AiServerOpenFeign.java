package com.ktb19.moviechatbot.feign;

import com.ktb19.moviechatbot.dto.AdditionalQueryRequest;
import com.ktb19.moviechatbot.dto.AiInfosResponse;
import com.ktb19.moviechatbot.dto.AiRecommendRequest;
import com.ktb19.moviechatbot.dto.AiRecommendResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient(name = "AiServer", url = "${AI_SERVICE_URL}")
public interface AiServerOpenFeign {

    @GetMapping("/infos")
    AiInfosResponse getInfos(@RequestParam String message);

    @PostMapping("/infos/additional")
    AiInfosResponse getInfosAdditional(@RequestBody AdditionalQueryRequest request);

    @PostMapping("/recommend")
    AiRecommendResponse getRecommend(@RequestBody AiRecommendRequest request);
}
