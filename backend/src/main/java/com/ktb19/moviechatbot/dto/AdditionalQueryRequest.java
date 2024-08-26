package com.ktb19.moviechatbot.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AdditionalQueryRequest {

    @Valid
    private ParsedQueryRequest parsedQuery;

    @Size(min = 1, max = 200)
    @Pattern(regexp = "^[가-힣a-zA-Z0-9 !#$%&'*+/=?`{|}~^.-]*$", message = "한글, 영어, 숫자, 특수문자만 입력할 수 있습니다.")
    private String message;
}
