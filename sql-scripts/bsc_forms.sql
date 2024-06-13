/* Copyright 2024 Google LLC
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License.
*/

SELECT __beneficiaryName as Name,
       __beneficiaryAddress as Address,
       __beneficiaryState as State,
       __beneficiaryZip as Zip,
       __beneficiaryDoB as DoB,

       __procCode as procCode,
       __procDesc as procDesc,
       __spFacilityName as spFacilityName,
       __issurerName as issurerName,
       __rpSpecialty as rpSpecialty,
       __rpJustification as rpJustification
       FROM `validation.pa_forms_bsc_flat`
-- where timestamp > cast('2023-05-02T19:00:00' as datetime)