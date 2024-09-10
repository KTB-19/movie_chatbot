package com.ktb19.moviechatbot.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class AiInfosResponse {

    private String movieName;
    private List<String> region;
    private String date;
    private String time;
    private String response;
}
