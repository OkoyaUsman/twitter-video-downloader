import re
import json
import argparse
import curl_cffi
import urllib.parse
from pathlib import Path

class TwitterVideoDownloader:
    def __init__(self):
        self.file_name = None
        self.frame_number = None
        self.tweet_id = None
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_tweet_id(self, tweet_url) -> str:
        try:
            if tweet_url[len(tweet_url)-1] != "/":
                tweet_url = tweet_url + "/"
            match = re.findall(r'https://x\.com/[^/]+/status/(\d+)', tweet_url)
            return match[0]
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_tweet(self, tweet_id):
        try:
            session = curl_cffi.Session(impersonate="chrome")
            headers = {
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'origin': 'https://x.com',
                'referer': 'https://x.com/',
                'X-Twitter-Active-User': 'yes',
                'X-Twitter-Client-Language': 'en',
            }
            session.headers.update(headers)
            query_tweet = "0aTrQMKgj95K791yXeNDRA"
            
            guest_token = session.post("https://api.x.com/1.1/guest/activate.json").json()["guest_token"]

            features = {
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "premium_content_api_read_enabled": False,
                "communities_web_enable_tweet_community_results_fetch": True,
                "c9s_tweet_anatomy_moderator_badge_enabled": True,
                "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
                "responsive_web_grok_analyze_post_followups_enabled": False,
                "responsive_web_jetfuel_frame": True,
                "responsive_web_grok_share_attachment_enabled": True,
                "responsive_web_grok_annotations_enabled": True,
                "articles_preview_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "responsive_web_twitter_article_tweet_consumption_enabled": True,
                "tweet_awards_web_tipping_enabled": False,
                "responsive_web_grok_show_grok_translated_post": False,
                "responsive_web_grok_analysis_button_from_backend": True,
                "post_ctas_fetch_enabled": True,
                "creator_subscriptions_quote_tweet_preview_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                "longform_notetweets_rich_text_read_enabled": True,
                "longform_notetweets_inline_media_enabled": True,
                "profile_label_improvements_pcf_label_in_post_enabled": True,
                "responsive_web_profile_redirect_enabled": False,
                "rweb_tipjar_consumption_enabled": False,
                "verified_phone_label_enabled": False,
                "responsive_web_grok_image_annotation_enabled": True,
                "responsive_web_grok_imagine_annotation_enabled": True,
                "responsive_web_grok_community_note_auto_translation_is_enabled": False,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_enhance_cards_enabled": False
            }

            variables = {
                "withCommunity": True,
                "includePromotedContent": True,
                "withVoice": True,
                "focalTweetId": tweet_id,
                "tweetId": tweet_id,
                "withBirdwatchNotes": True
            }

            fieldToggles = {
                "withArticleRichContentState": True,
                "withArticlePlainText": False
            }

            session.headers.update({"x-guest-token": guest_token})
            details = session.get(f"https://api.x.com/graphql/{query_tweet}/TweetResultByRestId?variables={urllib.parse.quote(json.dumps(variables))}&features={urllib.parse.quote(json.dumps(features))}&fieldToggles={urllib.parse.quote(json.dumps(fieldToggles))}")
            if details.status_code != 200:
                raise Exception(f'Failed to get tweet details. Status code: {details.status_code}. Tweet: {tweet_id}. Query: {query_tweet}')
            return details.json()
        except Exception as e:
            print(f"Error: {e}")
        return None

    def get_video(self, tweet_id, frame_number: int = 1) -> str:
        tweet_data = self.get_tweet(tweet_id)
        if not tweet_data:
            return
        try:
            medias = tweet_data.get("data", {}).get("tweetResult", {}).get("result", {}).get("legacy", {}).get("extended_entities", {}).get("media", [])
            if not medias:
                print("No media found in tweet")
                return
            media = medias[frame_number - 1]
            if "video_info" in media:
                variants = [v for v in media["video_info"]["variants"] if 'bitrate' in v]
                if variants:
                    variants.sort(key=lambda x: x['bitrate'], reverse=True)
                    return variants[0]['url']
                else:
                    print("No variants found in media")
                    return
            else:
                print("No video info found in media")
                return
        except Exception as e:
            print(f"Error: {e}")
            return

    def download_video(self, twitter_url: str, file_name: str = None, frame_number: int = 1):
        try:
            self.tweet_id = self.get_tweet_id(twitter_url)
            if not self.tweet_id:
                return
            if not file_name:
                file_name = f"{self.tweet_id}.mp4"
            if not file_name.endswith(".mp4"):
                file_name = file_name + ".mp4"
            if type(frame_number) != int:
                frame_number = 1
            video_url = self.get_video(self.tweet_id, frame_number)
            if not video_url:
                return
            response = curl_cffi.get(video_url)
            with open(self.output_dir / file_name, "wb") as f:
                f.write(response.content)
            print(f"Video downloaded successfully to {self.output_dir / file_name}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a video from Twitter/X using only the URL of the tweet and save it as a local .MP4 file in 'output' directory.")
    parser.add_argument("url", type=str, help="Twitter/X URL of the tweet to download.  e.g. https://x.com/OkoyaUsman/status/1692989065241469174")
    parser.add_argument("--file_name", type=str, required=False, help="Save Twitter/X video to this filename. e.g. twittervid.mp4")
    parser.add_argument("--frame", type=int, default=1, required=False, help="Frame number of the video to download. can be 1, 2, 3 or 4. Default is 1.")
    args = parser.parse_args()
    
    twitter = TwitterVideoDownloader()
    twitter.download_video(args.url, args.file_name, args.frame)