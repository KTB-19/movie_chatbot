package com.ktb19.moviechatbot.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.NotBlank;
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
public class MovieRunningTimesRequest {

    @NotBlank
    private String movieName;

    @NotBlank
    private String region;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd", timezone = "Asia/Seoul")
    @NotBlank
    private LocalDate date;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "HH:MM", timezone = "Asia/Seoul")
    private LocalTime time;

    public static MovieRunningTimesRequest of(AiInfosResponse aiInfosResponse) {
        return new MovieRunningTimesRequest(
                aiInfosResponse.getMovieName(),
                aiInfosResponse.getRegion(),
                LocalDate.parse(aiInfosResponse.getDate()),
                LocalTime.parse(aiInfosResponse.getTime())
        );
    }
}
