package com.ktb19.moviechatbot.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@Schema(description = "추가 메시지 파싱 응답")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class AdditionalParsedQueryResponse {

    @Schema(description = "영화 이름", example = "에이리언 : 로물루스")
    private String movieName;

    @Schema(description = "지역", example = "대구 동성로")
    private List<String> region;

    @Schema(description = "상영 날짜", example = "2024-08-14")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd", timezone = "Asia/Seoul")
    private LocalDate date;

    @Schema(description = "상영 시간", example = "17:00", type = "string")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "HH:mm", timezone = "Asia/Seoul")
    private LocalTime time;

    @Schema(description = "서비스 답변", example = "예매하기에 필요한 정보를 모두 제공해주셔서 감사합니다! " +
            "다음은 확인 질문입니다: 08/14(에) 17시에 대구 동성로에서 '에이리언 : 로물루스'을(를) " +
            "보시고 싶으신 게 맞으신가요?")
    private String message;

    public static AdditionalParsedQueryResponse of(QueryDto dto) {
        return new AdditionalParsedQueryResponse(
                dto.getMovieName(),
                dto.getRegion(),
                dto.getDate(),
                dto.getTime(),
                dto.getMessage()
        );
    }

}
