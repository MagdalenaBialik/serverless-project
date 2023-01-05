resource "aws_s3_bucket" "bucket" {
  bucket = "${var.app_name}-photo-bucket"

  tags = {
    Name = "${var.app_name}-photo-bucket"
  }
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.bucket.id
  acl    = "private"
}

resource "aws_s3_object" "object" {
  bucket   = aws_s3_bucket.bucket.bucket
  for_each = fileset(local.pics_directory_path, "**")
  source   = "${local.pics_directory_path}${each.value}"
  etag     = filemd5("${local.pics_directory_path}${each.value}")
  key      = each.value
}
