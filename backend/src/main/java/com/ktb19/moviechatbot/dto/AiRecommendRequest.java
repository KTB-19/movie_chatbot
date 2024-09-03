package com.ktb19.moviechatbot.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;
import java.util.Map;

import static com.ktb19.moviechatbot.constant.Constants.PATTERN_JSONFORMAT_DATE;
import static com.ktb19.moviechatbot.constant.Constants.PATTERN_JSONFORMAT_TIME;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class AiRecommendRequest {

    private String movieName;

    private String region;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = PATTERN_JSONFORMAT_DATE, timezone = "Asia/Seoul")
    private LocalDate date;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = PATTERN_JSONFORMAT_TIME, timezone = "Asia/Seoul")
    private LocalTime time;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = PATTERN_JSONFORMAT_TIME, timezone = "Asia/Seoul")
    private Map<String, List<LocalTime>> timesPerTheaterNameMap;
}
