//------------------------------------------------------------------------------
// Project:  arrayfunc
// Module:   aany_simd_x86.h
// Purpose:  Calculate the aany of values in an array.
//           This file provides an SIMD version of the functions.
// Language: C
// Date:     16-Apr-2019
// Ver:      27-Mar-2020.
//
//------------------------------------------------------------------------------
//
//   Copyright 2014 - 2020    Michael Griffin    <m12.griffin@gmail.com>
//
//   Licensed under the Apache License, Version 2.0 (the "License");
//   you may not use this file except in compliance with the License.
//   You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
//   Unless required by applicable law or agreed to in writing, software
//   distributed under the License is distributed on an "AS IS" BASIS,
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//   See the License for the specific language governing permissions and
//   limitations under the License.
//
//------------------------------------------------------------------------------


signed int aany_eq_signed_char_simd(Py_ssize_t arraylen, signed char *data, signed char param1);
signed int aany_gt_signed_char_simd(Py_ssize_t arraylen, signed char *data, signed char param1);
signed int aany_ge_signed_char_simd(Py_ssize_t arraylen, signed char *data, signed char param1);
signed int aany_lt_signed_char_simd(Py_ssize_t arraylen, signed char *data, signed char param1);
signed int aany_le_signed_char_simd(Py_ssize_t arraylen, signed char *data, signed char param1);
signed int aany_ne_signed_char_simd(Py_ssize_t arraylen, signed char *data, signed char param1);
signed int aany_eq_unsigned_char_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1);
signed int aany_gt_unsigned_char_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1);
signed int aany_ge_unsigned_char_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1);
signed int aany_lt_unsigned_char_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1);
signed int aany_le_unsigned_char_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1);
signed int aany_ne_unsigned_char_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1);
signed int aany_eq_signed_short_simd(Py_ssize_t arraylen, signed short *data, signed short param1);
signed int aany_gt_signed_short_simd(Py_ssize_t arraylen, signed short *data, signed short param1);
signed int aany_ge_signed_short_simd(Py_ssize_t arraylen, signed short *data, signed short param1);
signed int aany_lt_signed_short_simd(Py_ssize_t arraylen, signed short *data, signed short param1);
signed int aany_le_signed_short_simd(Py_ssize_t arraylen, signed short *data, signed short param1);
signed int aany_ne_signed_short_simd(Py_ssize_t arraylen, signed short *data, signed short param1);
signed int aany_eq_unsigned_short_simd(Py_ssize_t arraylen, unsigned short *data, unsigned short param1);
signed int aany_gt_unsigned_short_simd(Py_ssize_t arraylen, unsigned short *data, unsigned short param1);
signed int aany_ge_unsigned_short_simd(Py_ssize_t arraylen, unsigned short *data, unsigned short param1);
signed int aany_lt_unsigned_short_simd(Py_ssize_t arraylen, unsigned short *data, unsigned short param1);
signed int aany_le_unsigned_short_simd(Py_ssize_t arraylen, unsigned short *data, unsigned short param1);
signed int aany_ne_unsigned_short_simd(Py_ssize_t arraylen, unsigned short *data, unsigned short param1);
signed int aany_eq_signed_int_simd(Py_ssize_t arraylen, signed int *data, signed int param1);
signed int aany_gt_signed_int_simd(Py_ssize_t arraylen, signed int *data, signed int param1);
signed int aany_ge_signed_int_simd(Py_ssize_t arraylen, signed int *data, signed int param1);
signed int aany_lt_signed_int_simd(Py_ssize_t arraylen, signed int *data, signed int param1);
signed int aany_le_signed_int_simd(Py_ssize_t arraylen, signed int *data, signed int param1);
signed int aany_ne_signed_int_simd(Py_ssize_t arraylen, signed int *data, signed int param1);
signed int aany_eq_unsigned_int_simd(Py_ssize_t arraylen, unsigned int *data, unsigned int param1);
signed int aany_gt_unsigned_int_simd(Py_ssize_t arraylen, unsigned int *data, unsigned int param1);
signed int aany_ge_unsigned_int_simd(Py_ssize_t arraylen, unsigned int *data, unsigned int param1);
signed int aany_lt_unsigned_int_simd(Py_ssize_t arraylen, unsigned int *data, unsigned int param1);
signed int aany_le_unsigned_int_simd(Py_ssize_t arraylen, unsigned int *data, unsigned int param1);
signed int aany_ne_unsigned_int_simd(Py_ssize_t arraylen, unsigned int *data, unsigned int param1);
signed int aany_eq_float_simd(Py_ssize_t arraylen, float *data, float param1);
signed int aany_gt_float_simd(Py_ssize_t arraylen, float *data, float param1);
signed int aany_ge_float_simd(Py_ssize_t arraylen, float *data, float param1);
signed int aany_lt_float_simd(Py_ssize_t arraylen, float *data, float param1);
signed int aany_le_float_simd(Py_ssize_t arraylen, float *data, float param1);
signed int aany_ne_float_simd(Py_ssize_t arraylen, float *data, float param1);
signed int aany_eq_double_simd(Py_ssize_t arraylen, double *data, double param1);
signed int aany_gt_double_simd(Py_ssize_t arraylen, double *data, double param1);
signed int aany_ge_double_simd(Py_ssize_t arraylen, double *data, double param1);
signed int aany_lt_double_simd(Py_ssize_t arraylen, double *data, double param1);
signed int aany_le_double_simd(Py_ssize_t arraylen, double *data, double param1);
signed int aany_ne_double_simd(Py_ssize_t arraylen, double *data, double param1);


