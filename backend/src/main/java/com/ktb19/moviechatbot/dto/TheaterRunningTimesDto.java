package com.ktb19.moviechatbot.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.sql.Time;
import java.time.LocalTime;
import java.util.List;

import static com.ktb19.moviechatbot.constant.Constants.PATTERN_JSONFORMAT_TIME;

@Getter
@Setter
@AllArgsConstructor
public class TheaterRunningTimesDto {

    private String theaterName;

    private int count;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = PATTERN_JSONFORMAT_TIME, timezone = "Asia/Seoul")
    private List<LocalTime> times;

}
