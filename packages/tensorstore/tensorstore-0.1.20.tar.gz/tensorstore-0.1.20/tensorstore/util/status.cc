// Copyright 2020 The TensorStore Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "tensorstore/util/status.h"

#include <cstdio>
#include <exception>
#include <memory>
#include <ostream>
#include <string>
#include <string_view>
#include <system_error>  // NOLINT
#include <utility>

#include "absl/status/status.h"
#include "absl/strings/str_cat.h"
#include "tensorstore/internal/source_location.h"

namespace tensorstore {

absl::Status MaybeAnnotateStatus(const absl::Status& status,
                                 std::string_view message) {
  if (status.ok()) return status;
  if (status.message().empty()) {
    return absl::Status(status.code(), message);
  }
  return absl::Status(status.code(),
                      absl::StrCat(message, ": ", status.message()));
}

namespace internal {
[[noreturn]] void FatalStatus(const char* message, const absl::Status& status,
                              SourceLocation loc) {
  std::fprintf(stderr, "%s:%d: %s: %s\n", loc.file_name(), loc.line(), message,
               status.ToString().c_str());
  std::terminate();
}

}  // namespace internal
}  // namespace tensorstore
