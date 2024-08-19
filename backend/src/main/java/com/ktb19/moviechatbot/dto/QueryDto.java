package com.ktb19.moviechatbot.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class QueryDto {

    private String movieName;
    private String region;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd", timezone = "Asia/Seoul")
    private LocalDate date;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "HH:mm", timezone = "Asia/Seoul")
    private LocalTime time;

    private String message;

    public static QueryDto of(AiInfosResponse aiInfosResponse) {
        return new QueryDto(
                aiInfosResponse.getMovieName(),
                aiInfosResponse.getRegion(),
                LocalDate.parse(aiInfosResponse.getDate()),
                LocalTime.parse(aiInfosResponse.getTime()),
                aiInfosResponse.getResponse()
        );
    }
}
